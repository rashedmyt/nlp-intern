import 'package:flutter/material.dart';
import 'package:placement/screens/chat_page.dart';
import 'package:placement/utils.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:validators/validators.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _scaffoldState = GlobalKey<ScaffoldState>();
  final _formKey = GlobalKey<FormState>();
  FocusNode focusNode = FocusNode();
  TextEditingController _nameController = TextEditingController();
  TextEditingController _ipController = TextEditingController();

  @override
  void dispose() {
    focusNode.dispose();
    _nameController.dispose();
    _ipController.dispose();
    super.dispose();
  }

  Future<bool> storeUser() async {
    if (_formKey.currentState.validate()) {
      _scaffoldState.currentState.showSnackBar(
        SnackBar(
          content: Text('All Valid'),
        ),
      );
      final prefs = await SharedPreferences.getInstance();
      return await prefs.setString('username', _nameController.text);
    }

    _scaffoldState.currentState.showSnackBar(
      SnackBar(
        content: Text('Something is missing'),
      ),
    );

    return false;
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
                controller: _nameController,
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
                  FocusScope.of(context).requestFocus(focusNode);
                },
              ),
              SizedBox(
                height: 20,
              ),
              TextFormField(
                controller: _ipController,
                focusNode: focusNode,
                decoration: InputDecoration(labelText: 'IP Address'),
                validator: (value) {
                  return isIP(value) ? null : 'Enter a Valid IP';
                },
                onFieldSubmitted: (value) async {
                  var res = await storeUser();
                  if (res) {
                    var msg = await initialRequest(
                      url: "http://${_ipController.text}:7150/parse",
                    );
                    Navigator.of(context).pushReplacement(MaterialPageRoute(
                        builder: (context) => ChatPage(initMsg: msg)));
                  } else {
                    showAboutDialog(
                      context: context,
                      children: [
                        Text('Some Error ocurred while storing username')
                      ],
                    );
                  }
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
