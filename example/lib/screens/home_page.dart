import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:validators/validators.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _scaffoldState = GlobalKey<ScaffoldState>();
  final _formKey = GlobalKey<FormState>();
  FocusNode focusNode;
  String username;

  @override
  void initState() {
    super.initState();
    focusNode = FocusNode();
    username = '';
  }

  @override
  void dispose() {
    focusNode.dispose();
    super.dispose();
  }

  void storeUser() async {
    var text = '';
    final prefs = await SharedPreferences.getInstance();

    if (_formKey.currentState.validate()) {
      text = 'All valid';
      prefs.setString('username', username);
    } else {
      text = 'Something is missing';
    }

    _scaffoldState.currentState.showSnackBar(
      SnackBar(
        content: Text(text),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldState,
      body: Container(
        margin: EdgeInsets.symmetric(horizontal: 18),
        child: Form(
          autovalidate: true,
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              TextFormField(
                textInputAction: TextInputAction.next,
                decoration: InputDecoration(
                  labelText: 'Name',
                ),
                validator: (value) {
                  if (value.length < 4)
                    return 'Minimum 4 characters.';
                  else if (isAlpha(value))
                    return null;
                  else
                    return 'No special characters';
                },
                onFieldSubmitted: (value) {
                  username = value;
                  FocusScope.of(context).requestFocus(focusNode);
                },
              ),
              SizedBox(
                height: 20,
              ),
              TextFormField(
                focusNode: focusNode,
                decoration: InputDecoration(labelText: 'IP Address'),
                validator: (value) {
                  return isIP(value) ? null : 'Enter a Valid IP';
                },
                onFieldSubmitted: (value) {
                  storeUser();
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
