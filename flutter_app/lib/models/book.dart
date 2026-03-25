class Book {
  // Create book default constructor
  Book({
    required this.id,
    required this.isbn,
    required this.title,
    required this.author,
    required this.coverImage,
    required this.quantity,
    required this.insertedDate,
  });

  int id;
  int quantity;
  String isbn;
  String title;
  String author;
  String insertedDate;
  String coverImage;

  // Create book's factory constructor
  factory Book.fromJson(Map<String, dynamic> json) {
    return Book(
      id: json['id'] as int,
      isbn: json['isbn'] as String,
      title: json['title'] as String,
      author: json['author'] as String,
      quantity: json['quantity'] as int,
      insertedDate: json['inserted_date'] as String,
      coverImage: json['cover_image'] as String,
    );
  }

  // Convert books object to JSON map
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'isbn': isbn,
      'title': title,
      'author': author,
      'quantity': quantity,
      'inserted_date': insertedDate,
      'cover_image': coverImage,
    };
  }
}
