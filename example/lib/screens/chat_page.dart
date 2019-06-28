import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:placement/utils.dart';

class ChatPage extends StatefulWidget {
  final RequestResponse initMsg;

  ChatPage({@required this.initMsg});

  @override
  _ChatPageState createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text(widget.initMsg.text),
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.delete),
        onPressed: () async {
          SystemChannels.platform.invokeMethod('SystemNavigator.pop');
        },
      ),
    );
  }
}
