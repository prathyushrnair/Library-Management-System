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

    def handle(self, *args, **options):
        force = options["force"]
        updated = 0
        skipped = 0
        failed = 0

        books = Book.objects.all().order_by("id")

        for book in books:
            # Skip existing images unless --force is provided.
            if book.cover_image and not force:
                skipped += 1
                continue

            query = urllib.parse.urlencode(
                {
                    "title": book.title,
                    "author": book.author,
                    "limit": 1,
                }
            )
            search_url = f"https://openlibrary.org/search.json?{query}"

            try:
                req = urllib.request.Request(
                    search_url,
                    headers={"User-Agent": "LibraryManagementSystem/1.0"},
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except Exception:
                failed += 1
                self.stdout.write(
                    self.style.WARNING(f"[FAILED] Search request for: {book.title}")
                )
                continue

            docs = data.get("docs", [])
            if not docs:
                failed += 1
                self.stdout.write(
                    self.style.WARNING(f"[FAILED] No cover found: {book.title}")
                )
                continue

            cover_id = docs[0].get("cover_i")
            if not cover_id:
                failed += 1
                self.stdout.write(
                    self.style.WARNING(f"[FAILED] No cover id: {book.title}")
                )
                continue

            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

            try:
                req = urllib.request.Request(
                    cover_url,
                    headers={"User-Agent": "LibraryManagementSystem/1.0"},
                )
                with urllib.request.urlopen(req, timeout=20) as resp:
                    image_bytes = resp.read()
            except Exception:
                failed += 1
                self.stdout.write(
                    self.style.WARNING(f"[FAILED] Cover download: {book.title}")
                )
                continue

            if not image_bytes:
                failed += 1
                self.stdout.write(
                    self.style.WARNING(f"[FAILED] Empty cover bytes: {book.title}")
                )
                continue

            filename = f"official_{book.isbn}.jpg"
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
