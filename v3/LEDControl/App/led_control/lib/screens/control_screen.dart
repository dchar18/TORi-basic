import 'package:flutter/material.dart';
import 'package:led_control/widgets/widgets.dart';
import 'package:http/http.dart';

class ControlScreen extends StatefulWidget {
  final String device;
  static String mode = "";

  ControlScreen({this.device});

  @override
  _ControlScreenState createState() => _ControlScreenState();

  static void setMode(String newMode) {
    mode = newMode;
  }
}

class _ControlScreenState extends State<ControlScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).primaryColor,
      appBar: myAppBar(context, widget.device),
      body: Container(
        width: MediaQuery.of(context).size.width,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Container(
              alignment: Alignment.center,
              padding: EdgeInsets.only(top: 10, bottom: 5, right: 15, left: 20),
              child: Row(
                children: [
                  Text(
                    "Current mode: ",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 25,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    ControlScreen.mode,
                    style: TextStyle(
                      color: Theme.of(context).accentColor,
                      fontSize: 25,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              child: modeList(widget.device),
            ),
          ],
        ),
      ),
    );
  }
}

void sendRequest(String device, String mode) async {
  print("Received " + device + ", entering mode: " + mode);
  String url;
  if (mode.contains("twinkle")) {
    mode = mode.replaceAll(" twinkle", "");
    print("current mode: " + mode);
    mode = "twinkle_" + mode;
  }
  if (device == "All") {
    url = "http://192.168.50.114:8181/" + mode.toLowerCase() + "/sync";
  } else {
    url = "http://192.168.50.114:8181/esp8266_" +
        device.toLowerCase() +
        "/" +
        mode.toLowerCase();
  }

  print("Using url: " + url);
  final response = await get(url);
  // print(response.body);
  print("Response: " + response.statusCode.toString());
}
