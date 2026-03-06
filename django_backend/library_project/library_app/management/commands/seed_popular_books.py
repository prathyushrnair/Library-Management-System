from django.core.management.base import BaseCommand

from library_app.models import Book


POPULAR_BOOKS_BY_GENRE = {
    "Fantasy": [
        ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling"),
        ("The Hobbit", "J.R.R. Tolkien"),
        ("The Fellowship of the Ring", "J.R.R. Tolkien"),
        ("A Game of Thrones", "George R.R. Martin"),
        ("The Name of the Wind", "Patrick Rothfuss"),
        ("The Way of Kings", "Brandon Sanderson"),
        ("Mistborn: The Final Empire", "Brandon Sanderson"),
        ("The Lion, the Witch and the Wardrobe", "C.S. Lewis"),
        ("The Last Unicorn", "Peter S. Beagle"),
        ("The Priory of the Orange Tree", "Samantha Shannon"),
    ],
    "Science Fiction": [
        ("Dune", "Frank Herbert"),
        ("Ender's Game", "Orson Scott Card"),
        ("Neuromancer", "William Gibson"),
        ("The Martian", "Andy Weir"),
        ("Foundation", "Isaac Asimov"),
        ("The Left Hand of Darkness", "Ursula K. Le Guin"),
        ("Snow Crash", "Neal Stephenson"),
        ("Do Androids Dream of Electric Sheep?", "Philip K. Dick"),
        ("Hyperion", "Dan Simmons"),
        ("Project Hail Mary", "Andy Weir"),
    ],
    "Mystery": [
        ("The Girl with the Dragon Tattoo", "Stieg Larsson"),
        ("Gone Girl", "Gillian Flynn"),
        ("The Da Vinci Code", "Dan Brown"),
        ("And Then There Were None", "Agatha Christie"),
        ("Murder on the Orient Express", "Agatha Christie"),
        ("Big Little Lies", "Liane Moriarty"),
        ("The Silent Patient", "Alex Michaelides"),
        ("In the Woods", "Tana French"),
        ("The Cuckoo's Calling", "Robert Galbraith"),
        ("Magpie Murders", "Anthony Horowitz"),
    ],
    "Thriller": [
        ("The Bourne Identity", "Robert Ludlum"),
        ("The Hunt for Red October", "Tom Clancy"),
        ("The Girl on the Train", "Paula Hawkins"),
        ("The Reversal", "Michael Connelly"),
        ("The Firm", "John Grisham"),
        ("The Lincoln Lawyer", "Michael Connelly"),
        ("Shutter Island", "Dennis Lehane"),
        ("I Am Pilgrim", "Terry Hayes"),
        ("The Day of the Jackal", "Frederick Forsyth"),
        ("Before I Go to Sleep", "S.J. Watson"),
    ],
    "Romance": [
        ("Pride and Prejudice", "Jane Austen"),
        ("Me Before You", "Jojo Moyes"),
        ("Outlander", "Diana Gabaldon"),
        ("The Notebook", "Nicholas Sparks"),
        ("The Time Traveler's Wife", "Audrey Niffenegger"),
        ("It Ends with Us", "Colleen Hoover"),
        ("Eleanor & Park", "Rainbow Rowell"),
        ("Red, White & Royal Blue", "Casey McQuiston"),
        ("The Rosie Project", "Graeme Simsion"),
        ("Beach Read", "Emily Henry"),
    ],
    "Historical Fiction": [
        ("All the Light We Cannot See", "Anthony Doerr"),
        ("The Book Thief", "Markus Zusak"),
        ("Wolf Hall", "Hilary Mantel"),
        ("The Pillars of the Earth", "Ken Follett"),
        ("Pachinko", "Min Jin Lee"),
        ("The Nightingale", "Kristin Hannah"),
        ("A Gentleman in Moscow", "Amor Towles"),
        ("The Help", "Kathryn Stockett"),
        ("The Tattooist of Auschwitz", "Heather Morris"),
        ("Hamnet", "Maggie O'Farrell"),
    ],
    "Biography": [
        ("The Diary of a Young Girl", "Anne Frank"),
        ("Long Walk to Freedom", "Nelson Mandela"),
        ("Steve Jobs", "Walter Isaacson"),
        ("Becoming", "Michelle Obama"),
        ("The Wright Brothers", "David McCullough"),
        ("Alexander Hamilton", "Ron Chernow"),
        ("Einstein: His Life and Universe", "Walter Isaacson"),
        ("When Breath Becomes Air", "Paul Kalanithi"),
        ("Open", "Andre Agassi"),
        ("Shoe Dog", "Phil Knight"),
    ],
    "Self-Help": [
        ("Atomic Habits", "James Clear"),
        ("The 7 Habits of Highly Effective People", "Stephen R. Covey"),
        ("How to Win Friends and Influence People", "Dale Carnegie"),
        ("Think and Grow Rich", "Napoleon Hill"),
        ("The Power of Now", "Eckhart Tolle"),
        ("The Subtle Art of Not Giving a F*ck", "Mark Manson"),
        ("Deep Work", "Cal Newport"),
        ("Grit", "Angela Duckworth"),
        ("Mindset", "Carol S. Dweck"),
        ("Can't Hurt Me", "David Goggins"),
    ],
    "Horror": [
        ("It", "Stephen King"),
        ("The Shining", "Stephen King"),
        ("Dracula", "Bram Stoker"),
        ("Frankenstein", "Mary Shelley"),
        ("Bird Box", "Josh Malerman"),
        ("The Exorcist", "William Peter Blatty"),
        ("House of Leaves", "Mark Z. Danielewski"),
        ("Mexican Gothic", "Silvia Moreno-Garcia"),
        ("The Haunting of Hill House", "Shirley Jackson"),
        ("World War Z", "Max Brooks"),
    ],
    "Young Adult": [
        ("The Hunger Games", "Suzanne Collins"),
        ("The Fault in Our Stars", "John Green"),
        ("Divergent", "Veronica Roth"),
        ("The Maze Runner", "James Dashner"),
        ("The Giver", "Lois Lowry"),
        ("Percy Jackson and the Lightning Thief", "Rick Riordan"),
        ("Six of Crows", "Leigh Bardugo"),
        ("Legend", "Marie Lu"),
        ("Thirteen Reasons Why", "Jay Asher"),
        ("To All the Boys I've Loved Before", "Jenny Han"),
    ],
}


class Command(BaseCommand):
    help = "Seed 10 popular books for each genre."

    def handle(self, *args, **options):
        cover_images = [
            "Images/BooksCover/TheArtOfWar.jpg",
            "Images/BooksCover/The48LawsOfPower.jpg",
            "Images/BooksCover/YourNextFiveMoves.jpg",
            "Images/BooksCover/Oromay.jpg",
            "Images/BooksCover/YetenbitKetero.jpg",
            "Images/BooksCover/64a96717-ee4e-46e8-bdd2-7409868073da-1683683373.jpg",
        ]

        created = 0
        updated = 0
        isbn_counter = 1

        for genre, books in POPULAR_BOOKS_BY_GENRE.items():
            for idx, (title, author) in enumerate(books):
                isbn = f"978{isbn_counter:010d}"
                defaults = {
                    "title": title,
                    "author": author,
                    "genre": genre,
                    "cover_image": cover_images[idx % len(cover_images)],
                    "quantity": 15,
                }
                _, is_created = Book.objects.update_or_create(
                    isbn=isbn,
                    defaults=defaults,
                )
                if is_created:
                    created += 1
                else:
                    updated += 1
                isbn_counter += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Catalog seeded. Created: {created}, Updated: {updated}, Total processed: {created + updated}"
            )
        )
