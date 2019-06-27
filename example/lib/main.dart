import 'package:flutter/material.dart';
import 'package:placement/screens/home_page.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() => runApp(PlacementApp());

class PlacementApp extends StatelessWidget {
  Future<bool> isUserAccountPresent() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.containsKey('username');
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "Placement Bot",
      home: FutureBuilder<bool>(
        future: isUserAccountPresent(),
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return snapshot.data
                ? Scaffold(
                    body: Center(
                      child: Text('Chatbot actions takes place here'),
                    ),
                  )
                : HomePage();
          } else {
            return Material(
              child: Center(
                child: CircularProgressIndicator(),
              ),
            );
          }
        },
      ),
    );
  }
}
