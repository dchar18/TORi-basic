import 'dart:math';

import 'package:flutter/material.dart';
import 'package:led_control/data/device_modes.dart';
import 'package:led_control/screens/add_device_screen.dart';
import 'package:led_control/screens/control_screen.dart';
import 'package:led_control/screens/door_sensor_control.dart';
import 'package:led_control/screens/rc_control_screen.dart';

List<String> devices = ["Door Sensor", "All", "Bed", "Desk", "RC Lambo"];

Widget deviceList() {
  return ListView.builder(
    scrollDirection: Axis.vertical,
    shrinkWrap: true,
    // padding: EdgeInsets.only(top: 15.0),
    itemCount: devices.length,
    itemBuilder: (BuildContext context, int index) {
      return DeviceTile(
        deviceName: devices[index],
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
          builder: (_) => deviceName == "RC Lambo"
              ? RCControlScreen(dc: new DeviceControl(this.deviceName))
              : deviceName == "Door Sensor"
                  ? DoorSensorControl()
                  : ControlScreen(dc: new DeviceControl(this.deviceName)),
        ),
      ),
      // child: Card(
      //   elevation: 8.0,
      //   margin: new EdgeInsets.symmetric(horizontal: 10.0, vertical: 6.0),
      //   child: Container(
      //     height: itemHeight,
      //     width: MediaQuery.of(context).size.width,
      //     decoration: BoxDecoration(
      //       color: Color.fromRGBO(64, 75, 96, 0.9),
      //     ),
      //     child: ListTile(
      //       contentPadding:
      //           EdgeInsets.symmetric(horizontal: 20.0, vertical: 10.0),
      //       leading: Container(
      //         padding: EdgeInsets.only(right: 12.0),
      //         decoration: new BoxDecoration(
      //           border: new Border(
      //             right: new BorderSide(
      //               width: 1.0,
      //               color: Colors.white24,
      //             ),
      //           ),
      //         ),
      //         child: icon(deviceName),
      //       ),
      //       title: Text(
      //         deviceName,
      //         style: TextStyle(
      //           color: Colors.grey[600],
      //           fontWeight: FontWeight.bold,
      //         ),
      //       ),
      //       trailing: Icon(
      //         Icons.keyboard_arrow_right,
      //         color: Colors.grey[600],
      //         size: 30.0,
      //       ),
      //     ),
      //   ),
      // ),
      child: Container(
        padding: EdgeInsets.symmetric(vertical: 10),
        height: itemHeight,
        margin: EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: Colors.white,
          // gradient: LinearGradient(
          //   begin: Alignment.topLeft,
          //   end: Alignment(0.8, 0.0),
          //   colors: getGradient(),
          // ),
          borderRadius: BorderRadius.circular(35),
        ),
        child: Container(
          alignment: Alignment.center,
          child: Text(
            deviceName,
            textAlign: TextAlign.center,
            style: TextStyle(
                fontSize: 30,
                color: Colors.grey[800],
                fontWeight: FontWeight.normal),
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ),
    );
  }

  List<List<Color>> gradients = [
    [const Color(0xff90caf9), const Color(0xff5d99c6)],
    [const Color(0xffe3f2fd), const Color(0xffb1bfca)],
    [const Color(0xffd1c4e9), const Color(0xffa094b7)],
  ];

  getGradient() {
    int rand = Random().nextInt(gradients.length);
    print("Random int: " + rand.toString());
    return gradients[rand];
  }
}

icon(String name) {
  if (name == 'All') {
    return Icon(Icons.auto_awesome_motion, color: Colors.grey[600]);
  } else if (name == 'Bed') {
    return Icon(Icons.single_bed_outlined, color: Colors.grey[600]);
  } else if (name == 'Desk') {
    return Icon(Icons.event_seat_outlined, color: Colors.grey[600]);
  } else if (name == 'RC Lambo') {
    return Icon(Icons.directions_car_outlined, color: Colors.grey[600]);
  }
}

Widget doorTile(BuildContext context) {
  final itemHeight = (MediaQuery.of(context).size.height) / 10;

  return GestureDetector(
    onTap: () => Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => DoorSensorControl(),
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
          "Door Sensor",
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

backgroundGradient() {
  return BoxDecoration(
    gradient: LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment(0.8, 0.0), // 10% of the width, so there are ten blinds.,
      colors: [const Color(0xff03a9f4), const Color(0xff007ac1)],
    ),
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
  "Snow",
  "Fire"
];

Widget modeList(String device) {
  return ListView.builder(
    shrinkWrap: true,
    padding: EdgeInsets.only(top: 5.0),
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
        // ControlScreen.setMode(modeName);
      },
      child: Container(
        padding: EdgeInsets.symmetric(vertical: 5),
        height: itemHeight,
        margin: EdgeInsets.all(10),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(25),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.5),
              spreadRadius: 5,
              blurRadius: 7,
              offset: Offset(0, 3),
            ),
          ],
        ),
        child: Container(
          alignment: Alignment.center,
          child: Text(
            modeName,
            textAlign: TextAlign.center,
            style: TextStyle(
                fontSize: 30,
                color: Colors.grey[800],
                fontWeight: FontWeight.normal),
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ),
    );
  }
}
