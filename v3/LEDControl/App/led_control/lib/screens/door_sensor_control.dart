import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:led_control/data/option.dart';
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

class OptionList extends StatefulWidget {
  @override
  _OptionListState createState() => _OptionListState();
}

class _OptionListState extends State<OptionList> {
  List<Option> options = [
    new Option("Off"),
    new Option("Red Stable"),
    new Option("Red Pulse"),
    new Option("Green Stable"),
    new Option("Green Pulse"),
  ];

  // Widget optionTemplate(option) {
  //   return Card(
  //     margin: EdgeInsets.symmetric(horizontal: 5, vertical: 8),
  //     // margin: EdgeInsets.fromLTRB(16, 16, 16, 0),
  //     child: Row(
  //       children: [
  //         Text(
  //           option.name,
  //           style: TextStyle(
  //             color: Colors.white,
  //             fontSize: 25.0,
  //             fontFamily: "Roboto",
  //             fontWeight: FontWeight.normal,
  //           ),
  //         ),
  //       ],
  //     ),
  //   );
  Widget optionTemplate(context, option) {
    double _height = 100.0;

    return Container(
      height: _height,
      width: MediaQuery.of(context).size.width,
      padding: EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      margin: EdgeInsets.symmetric(horizontal: 5, vertical: 10),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.centerLeft,
          end: Alignment.centerRight,
          colors: [Colors.blue, Colors.purple],
        ),
        borderRadius: BorderRadius.all(
          Radius.circular(20),
        ),
      ),
      // margin: EdgeInsets.fromLTRB(16, 16, 16, 0),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                option.name,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 30.0,
                  fontFamily: "Roboto",
                  fontWeight: FontWeight.normal,
                ),
              ),
              GestureDetector(
                onTap: () {
                  print("Old height: " + _height.toString());
                  if (_height == 100.0) {
                    _height = 200.0;
                  } else {
                    _height = 100.0;
                  }
                  print("New height: " + _height.toString());
                },
                child: Icon(
                  Icons.keyboard_arrow_down,
                  size: 35.0,
                  color: Colors.white,
                ),
              ),
            ],
          ),
          Row(
            children: [
              Text(
                "Used by:",
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 20.0,
                  fontFamily: "Roboto",
                  fontWeight: FontWeight.normal,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Color(0xFF2D2F41),
      child: Column(
        children: [
          Expanded(
            child: ListView(
              scrollDirection: Axis.vertical,
              children: options
                  .map((option) => optionTemplate(context, option))
                  .toList(),
            ),
          ),
        ],
      ),
    );
  }
}
