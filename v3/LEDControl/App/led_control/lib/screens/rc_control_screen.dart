import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:led_control/widgets/widgets.dart';
import 'package:shared_preferences/shared_preferences.dart';

// reference: https://flutter.dev/docs/cookbook/persistence/key-value

class RCControlScreen extends StatefulWidget {
  @override
  _RCControlScreenState createState() => _RCControlScreenState();
}

class _RCControlScreenState extends State<RCControlScreen> {
  double _redValue = 0;
  double _greenValue = 0;
  double _blueValue = 0;

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
              "Red: " + _redValue.round().toString(),
              style: TextStyle(
                color: Colors.red,
                fontSize: 25,
                fontWeight: FontWeight.bold,
              ),
            ),
            Slider(
              value: _redValue,
              min: 0,
              max: 255,
              label: _redValue.round().toString(),
              onChanged: (double value) {
                setState(() {
                  _redValue = value;
                });
              },
              onChangeEnd: (double value) => updateRGB(),
              activeColor: Colors.red,
              inactiveColor: Colors.red[300],
            ),
            SizedBox(height: 10),
            Text(
              "Green: " + _greenValue.round().toString(),
              style: TextStyle(
                color: Colors.green,
                fontSize: 25,
                fontWeight: FontWeight.bold,
              ),
            ),
            Slider(
              value: _greenValue,
              min: 0,
              max: 255,
              label: _greenValue.round().toString(),
              onChanged: (double value) {
                setState(() {
                  _greenValue = value;
                });
              },
              onChangeEnd: (double value) => updateRGB(),
              activeColor: Colors.green,
              inactiveColor: Colors.green[300],
            ),
            SizedBox(height: 10),
            Text(
              "Blue: " + _blueValue.round().toString(),
              style: TextStyle(
                color: Colors.blue,
                fontSize: 25,
                fontWeight: FontWeight.bold,
              ),
            ),
            Slider(
              value: _blueValue,
              min: 0,
              max: 255,
              label: _blueValue.round().toString(),
              onChanged: (double value) {
                setState(() {
                  _blueValue = value;
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
      _redValue = (pref.get('red') ?? 0);
      _greenValue = (pref.get('green') ?? 0);
      _blueValue = (pref.get('blue') ?? 0);
    });
  }

  updateRGB() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      prefs.setDouble('red', _redValue);
      prefs.setDouble('green', _greenValue);
      prefs.setDouble('blue', _blueValue);
    });
    sendRGB(_redValue.round().toString(), _greenValue.round().toString(),
        _blueValue.round().toString());
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
