import 'package:flutter/material.dart';
import 'package:led_control/widgets/widgets.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).primaryColor,
      appBar: myAppBar(context, "LED Control"),
      body: Container(
        child: deviceList(),
      ),
    );
  }
}
