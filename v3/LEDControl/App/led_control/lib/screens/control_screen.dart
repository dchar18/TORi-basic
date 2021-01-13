import 'package:flutter/material.dart';
import 'package:led_control/data/device_modes.dart';
import 'package:led_control/widgets/widgets.dart';
import 'package:http/http.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ControlScreen extends StatefulWidget {
  final DeviceControl dc;

  ControlScreen({this.dc});

  @override
  _ControlScreenState createState() => _ControlScreenState();
}

class _ControlScreenState extends State<ControlScreen> {
  @override
  void initState() {
    super.initState();
    _loadRGB();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).primaryColor,
      appBar: myAppBar(context, widget.dc.getName()),
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
                    widget.dc.getName(),
                    style: TextStyle(
                      color: Theme.of(context).accentColor,
                      fontSize: 25,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
            Column(
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
              ],
            ),
            Expanded(
              child: ListView.builder(
                shrinkWrap: true,
                padding: EdgeInsets.only(top: 15.0),
                itemCount: modes.length,
                itemBuilder: (BuildContext context, int index) {
                  final String mode = modes[index];
                  return GestureDetector(
                    onTap: () {
                      setState(() {
                        widget.dc.setMode(mode);
                      });
                    },
                    child: ModeTile(
                      modeName: mode,
                      device: widget.dc.getName(),
                    ),
                  );
                },
              ),
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
      widget.dc.setRed(pref.get(widget.dc.getName() + 'red') ?? 0.0);
      widget.dc.setGreen(pref.get(widget.dc.getName() + 'green') ?? 0.0);
      widget.dc.setBlue(pref.get(widget.dc.getName() + 'blue') ?? 0.0);
    });
  }

  updateRGB() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      print("Updating for: " + widget.dc.getName());
      if (widget.dc.getName() == "All") {
        for (int i = 0; i < devices.length; i++) {
          prefs.setDouble(devices[i] + 'red', widget.dc.getRed());
          prefs.setDouble(devices[i] + 'green', widget.dc.getGreen());
          prefs.setDouble(devices[i] + 'blue', widget.dc.getBlue());
        }
      } else {
        prefs.setDouble(widget.dc.getName() + 'red', widget.dc.getRed());
        prefs.setDouble(widget.dc.getName() + 'green', widget.dc.getGreen());
        prefs.setDouble(widget.dc.getName() + 'blue', widget.dc.getBlue());
      }

      print("Prefs: " + prefs.toString());
    });
    sendRGB(
        widget.dc.getName().toLowerCase(),
        widget.dc.getRed().round().toString(),
        widget.dc.getGreen().round().toString(),
        widget.dc.getBlue().round().toString());
  }

  // this function sends solid rgb values to a specific board/all boards
  sendRGB(String name, String red, String green, String blue) async {
    String combination = red + "/" + green + "/" + blue;
    String address = "http://192.168.50.114:8181/";
    if (name == "all") {
      address = address + "rgb/sync/" + combination;
    } else {
      address = address + "esp8266_" + name + "/rgb/" + combination;
    }
    print("Sending combination " + combination + " to " + address);

    final response = await get(address);
    // print(response.body);
    print("Response code: " + response.statusCode.toString());
  }
}

// this function is used to send a mode (not solid rgb) to a specific board or to all
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
