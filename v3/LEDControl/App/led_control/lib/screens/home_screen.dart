import 'package:flutter/material.dart';
import 'package:led_control/screens/door_sensor_control.dart';
import 'package:led_control/widgets/widgets.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        height: MediaQuery.of(context).size.height,
        width: MediaQuery.of(context).size.width,
        decoration: backgroundGradient(),
        child: Column(
          children: [
            SizedBox(height: 30),
            Container(
              height: 75,
              width: MediaQuery.of(context).size.width,
              padding: EdgeInsets.only(top: 20, left: 25),
              child: Text(
                "Devices",
                style: TextStyle(
                    color: Colors.white,
                    fontSize: 35,
                    fontWeight: FontWeight.normal,
                    fontFamily: 'Roboto'),
              ),
              alignment: Alignment.centerLeft,
            ),
            Expanded(child: deviceList()),
          ],
        ),
      ),
    );
  }
}
