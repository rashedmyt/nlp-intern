import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

const defaultURL = "http://192.168.0.5:7150/parse";
var headers = {
  "Content-Type": "application/json",
};

Future<RequestResponse> sendMessage(RequestResponse msg) async {
  final prefs = await SharedPreferences.getInstance();
  final url = prefs.getString('url') ?? defaultURL;

  final resp =
      await http.post(url, headers: headers, body: json.encode(msg.toJson()));
  if (resp.statusCode == 200) {
    return RequestResponse.fromJson(json.decode(resp.body));
  } else {
    return RequestResponse(
      text: "I'm not sure what you said. Can you be more specific?",
      frame: msg.frame,
    );
  }
}

Future<RequestResponse> initialRequest({String url}) async {
  final prefs = await SharedPreferences.getInstance();
  final payload = {
    "text": "Hi",
    "frame": {},
    "context": {
      "name": prefs.getString('username'),
    },
  };

  var temp = prefs.getString('url') ?? defaultURL;
  if (url != null && url != temp) {
    await prefs.setString('url', url);
    temp = url;
  }

  final resp =
      await http.post(temp, headers: headers, body: json.encode(payload));
  if (resp.statusCode == 200) {
    return RequestResponse.fromJson(json.decode(resp.body));
  } else {
    return RequestResponse(text: 'Hi', frame: {});
  }
}

class RequestResponse {
  final String text;
  final Map<String, dynamic> frame;

  RequestResponse({this.text, this.frame});

  factory RequestResponse.fromJson(Map<String, dynamic> json) =>
      RequestResponse(
        text: json['directives'][0]['payload']['text'],
        frame: json['frame'],
      );

  Map<String, dynamic> toJson() => {
        "text": text,
        "frame": frame,
      };
}
