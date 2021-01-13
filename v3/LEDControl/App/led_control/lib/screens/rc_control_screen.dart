import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:led_control/data/device_modes.dart';
import 'package:led_control/widgets/widgets.dart';
import 'package:shared_preferences/shared_preferences.dart';

// reference: https://flutter.dev/docs/cookbook/persistence/key-value

class RCControlScreen extends StatefulWidget {
  final DeviceControl dc;

  RCControlScreen({this.dc});

  @override
  _RCControlScreenState createState() => _RCControlScreenState();
}

class _RCControlScreenState extends State<RCControlScreen> {
  @override
  void initState() {
    super.initState();
    _loadRGB();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).primaryColor,
      appBar: myAppBar(context, "RC Control"),
      body: Container(
        padding: EdgeInsets.all(10),
        child: Column(
          children: [
            Text(
              "Red: " + widget.dc.getRed().round().toString(),
              style: TextStyle(
                color: Colors.red,
                fontSize: 25,
                fontWeight: FontWeight.bold,
              ),
            ),
            Slider(
              value: widget.dc.getRed(),
              min: 0,
              max: 255,
              label: widget.dc.getRed().round().toString(),
              onChanged: (double value) {
                setState(() {
                  widget.dc.setRed(value);
                });
              },
              onChangeEnd: (double value) => updateRGB(),
              activeColor: Colors.red,
              inactiveColor: Colors.red[300],
            ),
            SizedBox(height: 10),
            Text(
              "Green: " + widget.dc.getGreen().round().toString(),
              style: TextStyle(
                color: Colors.green,
                fontSize: 25,
                fontWeight: FontWeight.bold,
              ),
            ),
            Slider(
              value: widget.dc.getGreen(),
              min: 0,
              max: 255,
              label: widget.dc.getGreen().round().toString(),
              onChanged: (double value) {
                setState(() {
                  widget.dc.setGreen(value);
                });
              },
              onChangeEnd: (double value) => updateRGB(),
              activeColor: Colors.green,
              inactiveColor: Colors.green[300],
            ),
            SizedBox(height: 10),
            Text(
              "Blue: " + widget.dc.getBlue().round().toString(),
              style: TextStyle(
                color: Colors.blue,
                fontSize: 25,
                fontWeight: FontWeight.bold,
              ),
            ),
            Slider(
              value: widget.dc.getBlue(),
              min: 0,
              max: 255,
              label: widget.dc.getBlue().round().toString(),
              onChanged: (double value) {
                setState(() {
                  widget.dc.setBlue(value);
                });
              },
              onChangeEnd: (double value) => updateRGB(),
              activeColor: Colors.blue,
              inactiveColor: Colors.blue[300],
            ),
            SizedBox(height: 20),
            Expanded(
              child: RCModeList(),
            ),
          ],
        ),
      ),
    );
  }

  _loadRGB() async {
    SharedPreferences pref = await SharedPreferences.getInstance();
    setState(() {
      print("Loading for: " + widget.dc.getName());
      widget.dc.setRed(pref.get(widget.dc.getName() + 'red') ?? 0);
      widget.dc.setGreen(pref.get(widget.dc.getName() + 'green') ?? 0);
      widget.dc.setBlue(pref.get(widget.dc.getName() + 'blue') ?? 0);
    });
  }

  updateRGB() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      print("Updating for: " + widget.dc.getName());
      prefs.setDouble(widget.dc.getName() + 'red', widget.dc.getRed());
      prefs.setDouble(widget.dc.getName() + 'green', widget.dc.getGreen());
      prefs.setDouble(widget.dc.getName() + 'blue', widget.dc.getBlue());
      print(prefs);
    });
    sendRGB(
        widget.dc.getRed().round().toString(),
        widget.dc.getGreen().round().toString(),
        widget.dc.getBlue().round().toString());
  }
}

sendRGB(String red, String green, String blue) async {
  String address = "http://192.168.50.114:8181/esp8266_rclambo/rgb/";
  String combination = red + "/" + green + "/" + blue;
  String url = address + combination;
  print("Sending combination " + combination + " to " + url);

  final response = await get(url);
  // print(response.body);
  print("Response code: " + response.statusCode.toString());
}

sendMode(String mode) async {
  String address = "http://192.168.50.114:8181/esp8266_rclambo/";
  String url = address + mode.toLowerCase();

  print("Sending " + mode.toLowerCase() + " to " + url);

  final response = await get(url);
  // print(response.body);
  print("Response code: " + response.statusCode.toString());
}

final List<String> RC_Modes = [
  "Off",
  "Rainbow",
];

Widget RCModeList() {
  return ListView.builder(
    shrinkWrap: true,
    padding: EdgeInsets.only(top: 15.0),
    itemCount: RC_Modes.length,
    itemBuilder: (BuildContext context, int index) {
      final String mode = RC_Modes[index];
      return RCModeTile(
        modeName: mode,
      );
    },
  );
}

class RCModeTile extends StatelessWidget {
  final String modeName;
  RCModeTile({@required this.modeName});

  @override
  Widget build(BuildContext context) {
    final itemHeight = (MediaQuery.of(context).size.height - 150) / 10;

    return GestureDetector(
      onTap: () {
        sendMode(modeName);
      },
      child: Container(
        padding: EdgeInsets.symmetric(vertical: 10),
        height: itemHeight,
        margin: EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: Colors.blue[50],
          borderRadius: BorderRadius.circular(25),
        ),
        child: Container(
          alignment: Alignment.center,
          child: Text(
            modeName,
            textAlign: TextAlign.center,
            style: TextStyle(
                fontSize: 30,
                color: Colors.grey[800],
                fontWeight: FontWeight.bold),
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ),
    );
  }
}
