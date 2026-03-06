import 'package:flutter/material.dart';
import 'package:flutter_app/App/app.dart';
import 'package:flutter_app/screens/authentication/views/signup.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';

import '../../providers/user_provider.dart';

class Login extends ConsumerStatefulWidget {
  const Login({Key? key}) : super(key: key);

  @override
  ConsumerState<Login> createState() => _LoginState();
}

class _LoginState extends ConsumerState<Login> {
  final _formKey = GlobalKey<FormState>();

  @override
  void initState() {
    super.initState();
    // Ensure login screen always starts in a logged-out state.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(userControllerProvider.notifier).logout();
    });
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: SingleChildScrollView(
          child: Form(
            key: _formKey,
            child: Stack(
              children: <Widget>[
                Column(
                  children: <Widget>[
                    SizedBox(
                      width: 600,
                      child: Image.asset(
                        'assets/shape2.png',
                        fit: BoxFit.fill,
                      ),
                    ),
                    const SizedBox(
                      height: 50,
                    ),
                    Padding(
                      padding: const EdgeInsets.all(30.0),
                      child: Column(
                        children: <Widget>[
                          IntrinsicHeight(
                            child: SizedBox(
                              width: 300,
                              child: Consumer(
                                builder: (context, ref, child) {
                                  return TextFormField(
                                    autofocus: true,
                                    decoration: InputDecoration(
                                      focusedBorder: OutlineInputBorder(
                                        borderSide: const BorderSide(
                                          color: Color(0xff2827e9),
                                          width: 3.0,
                                        ),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                      enabledBorder: OutlineInputBorder(
                                        borderSide: BorderSide(
                                          color: Colors.grey.shade400,
                                          width: 3.0,
                                        ),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                      errorBorder: OutlineInputBorder(
                                        borderSide: BorderSide(
                                          color: Colors.grey.shade400,
                                          width: 3.0,
                                        ),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                      focusedErrorBorder: OutlineInputBorder(
                                        borderSide: const BorderSide(
                                          color: Color(0xff2827e9),
                                          width: 3.0,
                                        ),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                      labelText: 'Enter Your UserName',
                                      labelStyle: TextStyle(
                                          color: Colors.grey.shade600),
                                      suffix: const Icon(
                                        Icons.text_format,
                                        color: Colors.grey,
                                      ),
                                    ),
                                    onChanged: (value) => ref
                                        .read(userControllerProvider.notifier)
                                        .setUsername(value),
                                    validator: (value) {
                                      if (value == null || value.isEmpty) {
                                        return "User name must not be empty";
                                      }
                                      return null;
                                    },
                                  );
                                },
                              ),
                            ),
                          ),
                          const SizedBox(
                            height: 20,
                          ),
                          IntrinsicHeight(
                            child: SizedBox(
                              width: 300,
                              child: Consumer(
                                builder: (context, ref, child) {
                                  return TextFormField(
                                    autofocus: true,
                                    obscureText: true,
                                    decoration: InputDecoration(
                                      focusedBorder: OutlineInputBorder(
                                        borderSide: const BorderSide(
                                          color: Color(0xff2827e9),
                                          width: 3.0,
                                        ),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                      enabledBorder: OutlineInputBorder(
                                        borderSide: BorderSide(
                                          color: Colors.grey.shade400,
                                          width: 3.0,
                                        ),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                      errorBorder: OutlineInputBorder(
                                        borderSide: BorderSide(
                                          color: Colors.grey.shade400,
                                          width: 3.0,
                                        ),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                      focusedErrorBorder: OutlineInputBorder(
                                        borderSide: const BorderSide(
                                          color: Color(0xff2827e9),
                                          width: 3.0,
                                        ),
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                      labelText: 'Enter Your Password',
                                      labelStyle: TextStyle(
                                          color: Colors.grey.shade600),
                                      suffix: const Icon(
                                        Icons.lock,
                                        color: Colors.grey,
                                      ),
                                    ),
                                    onChanged: (value) => ref
                                        .read(userControllerProvider.notifier)
                                        .setPassword(value),
                                    validator: (value) {
                                      if (value == null || value.isEmpty) {
                                        return "Password must not be empty";
                                      }
                                      return null;
                                    },
                                  );
                                },
                              ),
                            ),
                          ),
                          const SizedBox(
                            height: 10,
                          ),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.end,
                            children: <Widget>[
                              Consumer(
                                builder: (context, ref, child) {
                                  return TextButton(
                                    child: const Text('Forgot Password?'),
                                    onPressed: () {},
                                  );
                                },
                              ),
                            ],
                          ),
                          const SizedBox(
                            height: 15,
                          ),
                          Consumer(
                            builder: (context, ref, child) {
                              return TextButton(
                                onPressed: () async {
                                  if (_formKey.currentState!.validate()) {
                                    final navigator = Navigator.of(context);
                                    final messenger =
                                        ScaffoldMessenger.of(context);
                                    final errorMessage = await ref
                                        .read(userControllerProvider.notifier)
                                        .authenticateUser();
                                    if (errorMessage == null) {
                                      ref.invalidate(userDataProvider);
                                      if (!mounted) return;
                                      navigator.pushReplacement(
                                        MaterialPageRoute(
                                          builder: (BuildContext context) =>
                                              App(),
                                        ),
                                      );
                                    } else {
                                      if (!mounted) return;
                                      messenger
                                        ..hideCurrentSnackBar()
                                        ..showSnackBar(
                                          SnackBar(content: Text(errorMessage)),
                                        );
                                    }
                                  }
                                },
                                child: Container(
                                  width: 150,
                                  height: 46,
                                  decoration: BoxDecoration(
                                    borderRadius: BorderRadius.circular(10),
                                    gradient: const LinearGradient(
                                        begin: Alignment.topRight,
                                        end: Alignment.bottomLeft,
                                        colors: [
                                          Color(0xff5165ea),
                                          Color(0xff2827e9)
                                        ]),
                                  ),
                                  child: Center(
                                    child: Text(
                                      'Log In',
                                      style: GoogleFonts.delius(
                                        color: Colors.white,
                                        fontWeight: FontWeight.bold,
                                        fontSize: 18.0,
                                      ),
                                    ),
                                  ),
                                ),
                              );
                            },
                          ),
                          const SizedBox(height: 12),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Text("Don't have an account? "),
                              TextButton(
                                onPressed: () {
                                  Navigator.of(context).pushReplacement(
                                    MaterialPageRoute(
                                      builder: (BuildContext context) =>
                                          const SignUp(),
                                    ),
                                  );
                                },
                                child: const Text('Sign Up'),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
