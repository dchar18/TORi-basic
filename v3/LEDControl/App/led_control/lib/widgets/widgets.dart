import 'package:flutter/material.dart';
import 'package:led_control/screens/add_device_screen.dart';
import 'package:led_control/screens/control_screen.dart';

List<String> devices = ["All", "Bed", "Desk"];

Widget deviceList() {
  return ListView.builder(
    padding: EdgeInsets.only(top: 15.0),
    itemCount: devices.length,
    itemBuilder: (BuildContext context, int index) {
      final String deviceName = devices[index];
      return DeviceTile(
        deviceName: deviceName,
      );
    },
  );
}

class DeviceTile extends StatelessWidget {
  final String deviceName;
  DeviceTile({@required this.deviceName});

  @override
  Widget build(BuildContext context) {
    final itemHeight = (MediaQuery.of(context).size.height) / 10;

    return GestureDetector(
      onTap: () => Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ControlScreen(device: deviceName),
        ),
      ),
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
            deviceName,
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

Widget myAppBar(BuildContext context, String title) {
  return AppBar(
    backgroundColor: Theme.of(context).primaryColor,
    title: Text(
      title,
      style: TextStyle(fontSize: 25.0, fontWeight: FontWeight.bold),
    ),
    elevation: 0.0,
    actions: <Widget>[
      title == "LED Control"
          ? IconButton(
              padding: EdgeInsets.only(
                right: 10,
              ),
              icon: Icon(Icons.add),
              iconSize: 35.0,
              color: Colors.white,
              onPressed: () {
                Navigator.push(context,
                    MaterialPageRoute(builder: (context) => AddDevice()));
              },
            )
          : Container(),
    ],
  );
}

List<String> modes = [
  "Off",
  "Random",
  "Christmas",
  "Study",
  "Party",
  "Christmas twinkle",
  "Blue twinkle",
  "Green twinkle",
  "Snow"
];

Widget modeList(String device) {
  return ListView.builder(
    padding: EdgeInsets.only(top: 15.0),
    itemCount: modes.length,
    itemBuilder: (BuildContext context, int index) {
      final String mode = modes[index];
      return ModeTile(
        modeName: mode,
        device: device,
      );
    },
  );
}

class ModeTile extends StatelessWidget {
  final String modeName;
  final String device;
  ModeTile({@required this.device, @required this.modeName});

  @override
  Widget build(BuildContext context) {
    final itemHeight = (MediaQuery.of(context).size.height - 150) / 10;

    return GestureDetector(
      onTap: () {
        sendRequest(device, modeName);
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
