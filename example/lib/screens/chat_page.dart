import 'package:flutter/material.dart';
import 'package:placement/utils.dart';
import 'package:placement/screens/home_page.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ChatPage extends StatefulWidget {
  final RequestResponse initMsg;

  ChatPage({@required this.initMsg});

  @override
  _ChatPageState createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  List<Message> messageList = List<Message>();
  TextEditingController _inputTextController = TextEditingController();

  @override
  void initState() {
    super.initState();
    messageList.add(
      Message(
        msg: widget.initMsg,
        alignment: Alignment.centerLeft,
      ),
    );
  }

  @override
  void dispose() {
    _inputTextController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Placement Bot'),
        actions: <Widget>[
          IconButton(
            icon: Icon(Icons.exit_to_app),
            onPressed: () async {
              final logoutResult = await showDialog(
                context: context,
                builder: (context) {
                  return AlertDialog(
                    title: Text('Logout'),
                    content: Text('Are you sure you want to logout?'),
                    actions: <Widget>[
                      FlatButton(
                        child: Text('OK'),
                        onPressed: () => Navigator.of(context).pop(true),
                      ),
                      FlatButton(
                        child: Text('Cancel'),
                        onPressed: () => Navigator.of(context).pop(false),
                      ),
                    ],
                  );
                },
              );

              if (logoutResult) {
                final prefs = await SharedPreferences.getInstance();
                prefs.remove('username');
                prefs.remove('url');

                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(
                    builder: (context) => HomePage(),
                  ),
                );
              }
            },
          ),
        ],
      ),
      body: Column(
        children: <Widget>[
          Expanded(
            child: ListView.builder(
              reverse: true,
              itemCount: messageList.length,
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Align(
                    alignment: messageList.reversed.toList()[index].alignment,
                    child: Container(
                      decoration: BoxDecoration(
                        border: Border.all(),
                        borderRadius: BorderRadius.circular(5),
                      ),
                      padding: EdgeInsets.all(8),
                      child:
                          Text(messageList.reversed.toList()[index].msg.text),
                    ),
                  ),
                );
              },
            ),
          ),
          Container(
            padding: EdgeInsets.symmetric(horizontal: 15),
            margin: EdgeInsets.only(bottom: 20),
            child: TextField(
              controller: _inputTextController,
              decoration: InputDecoration(
                hintText: 'Enter Message',
                border: OutlineInputBorder(),
              ),
              onSubmitted: (value) async {
                if (value.isNotEmpty) {
                  final userMsg = RequestResponse(
                    text: value,
                    frame: messageList.last.msg.frame,
                  );

                  setState(() {
                    messageList.add(
                      Message(
                        msg: userMsg,
                        alignment: Alignment.centerRight,
                      ),
                    );
                  });

                  _inputTextController.clear();

                  final resp = await sendMessage(userMsg);

                  setState(() {
                    messageList.add(
                      Message(
                        msg: resp,
                        alignment: Alignment.centerLeft,
                      ),
                    );
                  });
                }
              },
            ),
          ),
        ],
      ),
    );
  }
}

class Message {
  final RequestResponse msg;
  final Alignment alignment;

  Message({
    @required this.msg,
    @required this.alignment,
  });
}
