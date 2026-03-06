import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import '../../utils/constants.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../models/user.dart';
import 'package:http/http.dart' as http;

final userControllerProvider =
    StateNotifierProvider<UserController, User>((ref) => UserController());

class UserController extends StateNotifier<User> {
  UserController() : super(User());

  void setUsername(String username) {
    state = state.copyWith(username: username);
  }

  void setFirstName(String firstName) {
    state = state.copyWith(firstName: firstName);
  }

  void setLastName(String lastName) {
    state = state.copyWith(lastName: lastName);
  }

  void setEmail(String email) {
    state = state.copyWith(email: email);
  }

  void setPassword(String password) {
    state = state.copyWith(password: password);
  }

  void setPhoto(Uint8List profileImageBytes, String profileImageName) {
    state = state.copyWith(
      profileImageBytes: profileImageBytes,
      profileImageName: profileImageName,
    );
  }

  Future<String?> createUser() async {
    try {
      final request =
          http.MultipartRequest('POST', Uri.parse('${baseUrl}register/'));
      request.fields['user_name'] = state.username;
      request.fields['first_name'] = state.firstName;
      request.fields['last_name'] = state.lastName;
      request.fields['email'] = state.email;
      request.fields['password'] = state.password;

      final profileImageBytes = state.profileImageBytes;
      final profileImageName = state.profileImageName;
      if (profileImageBytes != null && profileImageName != null) {
        final file = http.MultipartFile.fromBytes(
          'profile_image',
          profileImageBytes,
          filename: profileImageName,
        );
        request.files.add(file);
      }

      final response = await request.send();
      final responseBody = await response.stream.bytesToString();

      if (response.statusCode == 201) {
        return null;
      }

      if (response.statusCode == 400) {
        try {
          final data = jsonDecode(responseBody) as Map<String, dynamic>;
          if (data.containsKey('user_name')) {
            return (data['user_name'] as List).first.toString();
          }
          if (data.containsKey('email')) {
            return (data['email'] as List).first.toString();
          }
          final firstKey = data.keys.isNotEmpty ? data.keys.first : null;
          if (firstKey != null &&
              data[firstKey] is List &&
              (data[firstKey] as List).isNotEmpty) {
            return data[firstKey][0].toString();
          }
          if (data.containsKey('detail')) {
            return data['detail'].toString();
          }
        } catch (_) {}
        return 'Invalid signup details. Please review your input.';
      }

      String details = '';
      try {
        final data = jsonDecode(responseBody);
        if (data is Map<String, dynamic> && data['detail'] != null) {
          details = data['detail'].toString();
        }
      } catch (_) {}
      if (details.isEmpty) {
        details = 'HTTP ${response.statusCode}';
      }
      return 'Sign up failed. $details';
    } on SocketException {
      return 'Cannot connect to server. Make sure backend is running on $baseUrl';
    } catch (_) {
      return 'Unexpected signup error. Please try again.';
    }
  }

  Future<String?> authenticateUser() async {
    final prefs = await SharedPreferences.getInstance();
    // Always clear any stale tokens before a fresh login attempt.
    await prefs.remove('access');
    await prefs.remove('refresh');

    final response = await http.post(
      Uri.parse('${baseUrl}api/token/'),
      headers: {'Content-Type': 'application/json'},
      body:
          jsonEncode({'user_name': state.username, 'password': state.password}),
    );

    if (response.statusCode == 200) {
      final body = jsonDecode(response.body);
      // Save the user token locally in the users device.
      prefs.setString('access', body['access']);
      prefs.setString('refresh', body['refresh']);
      return null;
    }

    if (response.statusCode == 401) {
      await prefs.remove('access');
      await prefs.remove('refresh');
      return 'Incorrect username or password.';
    }

    await prefs.remove('access');
    await prefs.remove('refresh');
    return 'Unable to log in. Please try again.';
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access');
    await prefs.remove('refresh');
  }
}

final userDataProvider =
    FutureProvider<Map<String, dynamic>>((ref) => UserData().fetchUserData());

class UserData {
  Map<String, dynamic> userData = {};

  Future<Map<String, dynamic>> fetchUserData() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access');
    final response = await http.get(
      Uri.parse('${baseUrl}user/profile/'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      userData = json.decode(response.body);
      return userData;
    } else {
      return userData;
      // throw Exception('Failed to load user data');
    }
  }
}
