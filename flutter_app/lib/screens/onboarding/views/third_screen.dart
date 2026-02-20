import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class ThirdScreen extends StatelessWidget {
  const ThirdScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final imageHeight = size.height * 0.38;

    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 24, 16, 24),
          children: [
            SizedBox(
              height: imageHeight,
              child: Image.asset(
                'assets/Secured.png',
                fit: BoxFit.contain,
              ),
            ),
            const SizedBox(
              height: 16.0,
            ),
            Text(
              'Secured',
              textAlign: TextAlign.center,
              style: GoogleFonts.delius(
                fontWeight: FontWeight.bold,
                fontSize: 30.0,
              ),
            ),
            const SizedBox(
              height: 12.0,
            ),
            Text(
              'Rest assured knowing your data is protected. We employ token authentication to ensure the highest level of security for your account.',
              textAlign: TextAlign.center,
              style: GoogleFonts.delius(
                fontSize: 17.0,
              ),
            )
          ],
        ),
      ),
    );
  }
}
