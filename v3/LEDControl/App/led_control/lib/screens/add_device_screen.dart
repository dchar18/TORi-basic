import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:led_control/widgets/widgets.dart';

class AddDevice extends StatefulWidget {
  @override
  _AddDeviceState createState() => _AddDeviceState();
}

class _AddDeviceState extends State<AddDevice> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).accentColor,
      appBar: myAppBar(context, "New Device"),
      body: Container(
        child: Column(
          children: <Widget>[
            GestureDetector(
              onTap: () {
                print("Searching...");
              },
              child: Container(
                child: Text(
                  "Search",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 25.0,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                padding: EdgeInsets.all(10),
                margin: EdgeInsets.all(10),
                width: MediaQuery.of(context).size.width,
                height: 50,
                decoration: BoxDecoration(
                  color: Theme.of(context).primaryColor,
                  borderRadius: BorderRadius.all(
                    Radius.circular(20.0),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
