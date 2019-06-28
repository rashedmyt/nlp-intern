import 'package:flutter/material.dart';
import 'package:placement/screens/chat_page.dart';
import 'package:placement/screens/home_page.dart';
import 'package:placement/utils.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() => runApp(PlacementApp());

class PlacementApp extends StatelessWidget {
  Future<bool> isUserAccountPresent() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.containsKey('username');
  }

  Widget showHomePage(bool present) {
    if (present) {
      return FutureBuilder<RequestResponse>(
        future: initialRequest(),
        builder: (context, snapshot) {
          return snapshot.hasData
              ? ChatPage(initMsg: snapshot.data)
              : Material();
        },
      );
    }

    return HomePage();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "Placement Bot",
      home: FutureBuilder<bool>(
        future: isUserAccountPresent(),
        builder: (context, snapshot) {
          return snapshot.hasData ? showHomePage(snapshot.data) : Material();
        },
      ),
    );
  }
}
