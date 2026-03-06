import io
import textwrap

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from PIL import Image, ImageDraw, ImageFont

from library_app.models import Book


GENRE_COLORS = {
    "Fantasy": (97, 62, 198),
    "Science Fiction": (33, 150, 243),
    "Mystery": (66, 66, 66),
    "Thriller": (183, 28, 28),
    "Romance": (233, 30, 99),
    "Historical Fiction": (121, 85, 72),
    "Biography": (0, 131, 143),
    "Self-Help": (76, 175, 80),
    "Horror": (45, 45, 45),
    "Young Adult": (255, 152, 0),
    "General": (63, 81, 181),
}


class Command(BaseCommand):
    help = "Generate simple local book covers (title + author + genre) for all books."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Regenerate covers even if book already has a generated one.",
        )

    def handle(self, *args, **options):
        force = options["force"]
        updated = 0
        skipped = 0

        title_font = ImageFont.load_default()
        meta_font = ImageFont.load_default()

        for book in Book.objects.all().order_by("id"):
            has_generated = bool(book.cover_image and "generated_" in book.cover_image.name)
            if has_generated and not force:
                skipped += 1
                continue

            width, height = 600, 900
            bg_color = GENRE_COLORS.get(book.genre, GENRE_COLORS["General"])
            image = Image.new("RGB", (width, height), bg_color)
            draw = ImageDraw.Draw(image)

            # Top tag strip
            draw.rectangle((0, 0, width, 120), fill=(255, 255, 255))
            draw.text((24, 42), (book.genre or "General").upper(), fill=(20, 20, 20), font=meta_font)

            # Title block
            title_lines = textwrap.wrap(book.title, width=22)[:5]
            y = 180
            for line in title_lines:
                draw.text((36, y), line, fill=(255, 255, 255), font=title_font)
                y += 30

            # Author + ISBN footer
            draw.rectangle((0, height - 160, width, height), fill=(255, 255, 255))
            draw.text((24, height - 120), f"Author: {book.author}", fill=(20, 20, 20), font=meta_font)
            draw.text((24, height - 80), f"ISBN: {book.isbn}", fill=(20, 20, 20), font=meta_font)

            # Encode and save
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=90)
            buffer.seek(0)

            filename = f"generated_{book.isbn}.jpg"
            book.cover_image.save(
                filename,
                ContentFile(buffer.read()),
                save=True,
            )

            updated += 1
            self.stdout.write(self.style.SUCCESS(f"[UPDATED] {book.title}"))

        self.stdout.write(
            self.style.SUCCESS(f"Done. Updated: {updated}, Skipped: {skipped}")
        )
