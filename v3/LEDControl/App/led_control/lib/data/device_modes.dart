import 'dart:collection';

class Modes {
  String deviceName;
  HashMap<String, dynamic> settings;
  List<String> devices;

  Modes(String name) {
    this.deviceName = name;
    settings = new Map();
    devices = ["All", "Bed", "Desk", "RC Lambo"];
    devices.forEach((element) {
      addDevice(element);
    });
  }

  String getName() {
    return this.deviceName;
  }

  addDevice(String name) {
    settings.putIfAbsent(
        name,
        () => {
              'mode': 'off',
              'rgb': {'red': 0, 'green': 0, 'blue': 0}
            });
  }

  getDeviceName(int index) {
    return devices[index];
  }

  getNumDevices() {
    return devices.length;
  }

  updateMode(String device, String mode) {
    settings[device]['mode'] = mode;
  }

  updateModeAll(String mode) {
    settings.forEach((key, value) {
      settings[key]['mode'] = mode;
    });
  }

  updateRGB(String device, double red, double green, double blue) {
    settings[device]['mode'] = 'rgb';
    settings[device]['rgb']['red'] = red;
    settings[device]['rgb']['green'] = green;
    settings[device]['rgb']['blue'] = blue;
  }

  getDeviceMode(String device) {
    return settings[device]['mode'];
  }

  getRedValue(String device) {
    return settings[device]['rgb']['red'];
  }

  getGreenValue(String device) {
    return settings[device]['rgb']['green'];
  }

  getBlueValue(String device) {
    return settings[device]['rgb']['blue'];
  }
}

class DeviceControl {
  String deviceName;
  String mode;
  var rgb;

  DeviceControl(String name) {
    this.deviceName = name;
    this.mode = "off";
    this.rgb = new Map();
    this.rgb['red'] = 0.0;
    this.rgb['green'] = 0.0;
    this.rgb['blue'] = 0.0;
    this.rgb['brightness'] = 65.0;
  }

  String getName() {
    return this.deviceName;
  }

  String getMode() {
    return this.mode;
  }

  void setMode(String mode) {
    this.mode = mode;
  }

  getRed() {
    return this.rgb['red'];
  }

  void setRed(double red) {
    this.rgb['red'] = red;
  }

  getGreen() {
    return this.rgb['green'];
  }

  void setGreen(double green) {
    this.rgb['green'] = green;
  }

  getBlue() {
    return this.rgb['blue'];
  }

  void setBlue(double blue) {
    this.rgb['blue'] = blue;
  }

  getBrightness() {
    return this.rgb['brightness'];
  }

  void setBrightness(double brightness) {
    this.rgb['brightness'] = brightness;
  }
}
