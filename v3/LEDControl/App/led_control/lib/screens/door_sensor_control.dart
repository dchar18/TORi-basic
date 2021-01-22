import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:led_control/widgets/widgets.dart';

class DoorSensorControl extends StatefulWidget {
  @override
  _DoorSensorControlState createState() => _DoorSensorControlState();
}

class _DoorSensorControlState extends State<DoorSensorControl> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).primaryColor,
      appBar: myAppBar(context, "Door Sensor"),
      body: optionList(),
    );
  }

  // "toggle": manually switch on/off flag to the opposite state
  // "keep off": set flag to "off" and turn sensor off
  // "keep on": set flag to "on" and turn sensor off
  // "reset": set flag to "on" and turn sensor on
  // List<String> options = ["Toggle", "Keep on", "Keep off", "Reset"];
  List<String> options = [
    "Off",
    "Red Stable",
    "Red Pulse",
    "Green Stable",
    "Green Pulse"
  ];
  Widget optionList() {
    return ListView.builder(
      shrinkWrap: true,
      padding: EdgeInsets.only(top: 15.0),
      itemCount: options.length,
      itemBuilder: (BuildContext context, int index) {
        final String option = options[index];
        return OptionTile(
          optionName: option,
        );
      },
    );
  }
}

class OptionTile extends StatelessWidget {
  final String optionName;
  OptionTile({@required this.optionName});

  @override
  Widget build(BuildContext context) {
    final itemHeight = (MediaQuery.of(context).size.height - 150) / 10;

    return GestureDetector(
      onTap: () {
        sendOption(optionName);
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
            optionName,
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

  // used exclusively for the door sensor board
  sendOption(String option) async {
    option = option.toLowerCase();
    option = option.replaceFirst(' ', '_');
    String address =
        "http://192.168.50.114:8181/esp8266_door/" + option.toLowerCase();

    print("Sending to " + address);
    final response = await get(address);
    print("Response code: " + response.statusCode.toString());
  }
}
