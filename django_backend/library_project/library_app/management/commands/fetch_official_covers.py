import json
import urllib.parse
import urllib.request

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from library_app.models import Book


class Command(BaseCommand):
    help = "Fetch official book covers from Open Library and update Book.cover_image."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing covers for all books.",
        )
        parser.add_argument(
            "--replace-generated",
            action="store_true",
            help="Replace only generated covers (generated_*.jpg) even without --force.",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=20,
            help="HTTP timeout in seconds (default: 20).",
        )

    def handle(self, *args, **options):
        force = options["force"]
        replace_generated = options["replace_generated"]
        timeout = options["timeout"]
        updated = 0
        skipped = 0
        failed = 0

        books = Book.objects.all().order_by("id")

        for book in books:
            has_cover = bool(book.cover_image)
            has_generated = has_cover and "generated_" in book.cover_image.name

            # Skip existing images unless --force or --replace-generated applies.
            if has_cover and not force and not (replace_generated and has_generated):
                skipped += 1
                continue

            cover_url = self._find_cover_url(book, timeout=timeout)
            if not cover_url:
                failed += 1
                self.stdout.write(
                    self.style.WARNING(f"[FAILED] No cover candidate: {book.title}")
                )
                continue

            try:
                req = urllib.request.Request(
                    cover_url,
                    headers={"User-Agent": "LibraryManagementSystem/1.0"},
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    image_bytes = resp.read()
            except Exception:
                failed += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"[FAILED] Cover download: {book.title} ({cover_url})"
                    )
                )
                continue

            if not image_bytes:
                failed += 1
                self.stdout.write(
                    self.style.WARNING(f"[FAILED] Empty cover bytes: {book.title}")
                )
                continue

            isbn_or_id = (book.isbn or str(book.id)).replace("/", "_")
            filename = f"official_{isbn_or_id}.jpg"
            book.cover_image.save(
                f"Images/BooksCover/{filename}",
                ContentFile(image_bytes),
                save=True,
            )
            updated += 1
            self.stdout.write(self.style.SUCCESS(f"[UPDATED] {book.title}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Updated: {updated}, Skipped: {skipped}, Failed: {failed}"
            )
        )

    def _find_cover_url(self, book, timeout=20):
        # 1) Fast path: direct ISBN cover lookup.
        isbn = (book.isbn or "").strip()
        if isbn:
            isbn_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg?default=false"
            if self._url_exists(isbn_url, timeout=timeout):
                return isbn_url

        # 2) Search fallback variants; then use cover id or OLID when available.
        title = (book.title or "").strip()
        author = (book.author or "").strip()
        normalized_title = title.replace("’", "'").replace("“", '"').replace("”", '"')
        normalized_author = author.replace("’", "'").replace("“", '"').replace("”", '"')

        query_variants = []
        if title and author and author.lower() != "unknown author":
            query_variants.append({"title": title, "author": author, "limit": 8})
            if normalized_title != title or normalized_author != author:
                query_variants.append(
                    {"title": normalized_title, "author": normalized_author, "limit": 8}
                )
        if title:
            query_variants.append({"title": title, "limit": 12})
            if normalized_title != title:
                query_variants.append({"title": normalized_title, "limit": 12})

        for params in query_variants:
            query = urllib.parse.urlencode(params)
            search_url = f"https://openlibrary.org/search.json?{query}"
            try:
                req = urllib.request.Request(
                    search_url,
                    headers={"User-Agent": "LibraryManagementSystem/1.0"},
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except Exception:
                continue

            docs = data.get("docs", [])
            for doc in docs:
                cover_id = doc.get("cover_i")
                if cover_id:
                    by_id = (
                        f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg?default=false"
                    )
                    if self._url_exists(by_id, timeout=timeout):
                        return by_id

                edition_keys = doc.get("edition_key") or []
                if edition_keys:
                    olid = edition_keys[0]
                    by_olid = (
                        f"https://covers.openlibrary.org/b/olid/{olid}-L.jpg?default=false"
                    )
                    if self._url_exists(by_olid, timeout=timeout):
                        return by_olid

        # 3) Secondary fallback: Google Books covers.
        google_cover = self._find_google_books_cover_url(
            title=title,
            author=author,
            timeout=timeout,
        )
        if google_cover:
            return google_cover

        return None

    def _find_google_books_cover_url(self, title, author, timeout=20):
        if not title:
            return None

        # Prefer title + author when author is meaningful, otherwise title only.
        if author and author.lower() != "unknown author":
            q = f'intitle:"{title}" inauthor:"{author}"'
        else:
            q = f'intitle:"{title}"'

        query = urllib.parse.urlencode({"q": q, "maxResults": 5})
        url = f"https://www.googleapis.com/books/v1/volumes?{query}"

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "LibraryManagementSystem/1.0"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception:
            return None

        items = data.get("items", [])
        for item in items:
            volume = item.get("volumeInfo", {})
            links = volume.get("imageLinks", {})
            for key in ("extraLarge", "large", "medium", "thumbnail", "smallThumbnail"):
                candidate = links.get(key)
                if not candidate:
                    continue
                candidate = candidate.replace("http://", "https://")
                if self._url_exists(candidate, timeout=timeout):
                    return candidate

        return None

    def _url_exists(self, url, timeout=20):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "LibraryManagementSystem/1.0"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return 200 <= resp.status < 300
        except Exception:
            return False
