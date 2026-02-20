import 'package:flutter/material.dart';

class BorrowedBooksScreen extends StatelessWidget {
  const BorrowedBooksScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Borrowed Books')),
      body: const Center(child: Text('Borrowed books placeholder')),
    );
  }
}
