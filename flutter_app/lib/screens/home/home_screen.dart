import 'package:flutter/material.dart';
import 'package:flutter_app/screens/home/vews/search_screen.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';

import '../../utils/constants.dart';
import '../providers/book_provider.dart';
import '../providers/user_provider.dart';
import 'vews/books_detail_screen.dart';
import 'widgets/custom_text_field.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Consumer(
      builder: (context, ref, child) {
        final user = ref.watch(userDataProvider);
        final books = ref.watch(bookDataProvider);
        return user.when(
          loading: () => const Center(
            child: CircularProgressIndicator(),
          ),
          error: (err, stack) => Text('Error: $err'),
          data: (userData) {
            final rawProfileImage = userData['profile_image'];
            final profileImage = rawProfileImage?.toString();
            final hasProfileImage = profileImage != null &&
                profileImage.isNotEmpty &&
                profileImage != 'null';
            return Scaffold(
              appBar: AppBar(
                backgroundColor: Colors.transparent,
                elevation: 0.0,
                automaticallyImplyLeading: false,
                bottom: PreferredSize(
                  preferredSize: const Size.fromHeight(180.0),
                  child: Column(
                    children: [
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 18.0),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  '👋 Hello, ${userData['first_name']}',
                                  style: GoogleFonts.delius(
                                    fontWeight: FontWeight.bold,
                                    color: smallTextColor,
                                    fontSize: 17.0,
                                  ),
                                ),
                                const SizedBox(
                                  height: 10.0,
                                ),
                                Text(
                                  'What Would you like \n to read today?',
                                  style: GoogleFonts.delius(
                                    fontSize: 23.0,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                            CircleAvatar(
                              radius: 26,
                              backgroundImage: hasProfileImage
                                  ? NetworkImage('$baseUrl$profileImage')
                                  : null,
                              child: hasProfileImage
                                  ? null
                                  : const Icon(Icons.person),
                            )
                          ],
                        ),
                      ),
                      const SizedBox(
                        height: 18.0,
                      ),
                      CustomTextField(
                        keyboardType: TextInputType.text,
                        suffixIcon: GestureDetector(
                          onTap: () async {
                            await ref
                                .read(searchBooksProvider)
                                .searchBooks(_controller.text)
                                .then(
                              (books) {
                                if (books.isNotEmpty) {
                                  Navigator.of(context).push(
                                    MaterialPageRoute(
                                      builder: (context) =>
                                          SearchResultsPage(books: books),
                                    ),
                                  );
                                }
                              },
                            );
                          },
                          child: const Icon(
                            Icons.search,
                            color: AppConst.kBkDark,
                          ),
                        ),
                        controller: _controller,
                        fillColor: Colors.white,
                        hintText: 'Search...',
                      )
                    ],
                  ),
                ),
              ),
              body: books.when(
                data: (bookData) {
                  if (bookData.isEmpty) {
                    return const Center(
                      child: Text('No books available right now.'),
                    );
                  }

                  return Padding(
                    padding: const EdgeInsets.only(left: 15.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding:
                              const EdgeInsets.only(left: 8.0, bottom: 8.0),
                          child: Text(
                            '${bookData.length} books available',
                            style: GoogleFonts.delius(
                              fontWeight: FontWeight.bold,
                              color: AppConst.kGreyLight,
                            ),
                          ),
                        ),
                        Expanded(
                          child: GridView.builder(
                            gridDelegate:
                                const SliverGridDelegateWithMaxCrossAxisExtent(
                              maxCrossAxisExtent: 180.0,
                              mainAxisSpacing: 20.0,
                              mainAxisExtent: 230.0,
                            ),
                            physics: const BouncingScrollPhysics(),
                            itemCount: bookData.length,
                            itemBuilder: (context, index) {
                              final book = bookData[index];
                              return GestureDetector(
                                onTap: () {
                                  Navigator.of(context).push(
                                    MaterialPageRoute(
                                      builder: (context) =>
                                          BookDetailPage(book: book),
                                    ),
                                  );
                                },
                                child: Container(
                                  width: 120,
                                  margin: const EdgeInsets.only(
                                    left: 6.0,
                                    right: 6.0,
                                  ),
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Expanded(
                                        child: ClipRRect(
                                          borderRadius:
                                              BorderRadius.circular(20.0),
                                          child: Image.network(
                                            '$baseUrl${book.cover_image}',
                                            fit: BoxFit.cover,
                                            width: double.infinity,
                                            errorBuilder:
                                                (context, error, stackTrace) {
                                              return Container(
                                                color: Colors.white,
                                                alignment: Alignment.center,
                                                child: const Icon(
                                                  Icons.menu_book_rounded,
                                                  color: AppConst.kGreyLight,
                                                  size: 34,
                                                ),
                                              );
                                            },
                                          ),
                                        ),
                                      ),
                                      const SizedBox(height: 6),
                                      Text(
                                        book.title,
                                        maxLines: 1,
                                        overflow: TextOverflow.ellipsis,
                                        style: GoogleFonts.delius(
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                      Text(
                                        book.author,
                                        maxLines: 1,
                                        overflow: TextOverflow.ellipsis,
                                        style: GoogleFonts.delius(
                                          color: AppConst.kGreyLight,
                                          fontSize: 12,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              );
                            },
                          ),
                        ),
                      ],
                    ),
                  );
                },
                error: (error, stackTrace) {
                  return Center(
                    child: Text(error.toString()),
                  );
                },
                loading: () {
                  return const Center(
                    child: CircularProgressIndicator(),
                  );
                },
              ),
            );
          },
        );
      },
    );
  }
}
