import requests, json
import os
import subprocess


def kelvin_to_F(kelvin):
    return int((kelvin - 273.15) * 1.8 + 32)


api_key = "2070c00d32fdfeaac43d863f958634a8"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = "Arlington Heights "
# city_name = "Chicago "
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

response = requests.get(complete_url)

x = response.json()

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
if x["cod"] != "404":

    # store the value of "main"
    # key in variable y
    y = x["main"]

    # store the value corresponding
    # to the "temp" key of y
    curr_temp_kelvin = y["temp"]
    # (0K − 273.15) × 9/5 + 32 = -459.7°F
    curr_temp_F = kelvin_to_F(curr_temp_kelvin)

    # store the value corresponding
    # to the "pressure" key of y
    current_pressure = y["pressure"]

    # store the value corresponding
    # to the "humidity" key of y
    current_humidity = y["humidity"]

    # store the value of "weather"
    # key in variable z
    z = x["weather"]

    # store the value corresponding
    # to the "description" key at
    # the 0th index of z
    weather_description = z[0]["description"]

    temp_min = kelvin_to_F(y["temp_min"])
    temp_max = kelvin_to_F(y["temp_max"])

    # print following values
    # print(" Temperature (in kelvin unit) = " +
    #       str(curr_temp_F) +
    #       "\n atmospheric pressure (in hPa unit) = " +
    #       str(current_pressure) +
    #       "\n humidity (in percentage) = " +
    #       str(current_humidity) +
    #       "\n description = " +
    #       str(weather_description))

    temp_range_text = " with a high of " + str(temp_max) + " and a low of " + str(temp_min) + " degrees fahrenheit "
    temp_text = "The temperature in " + city_name + "is " + str(curr_temp_F) + " degrees fahrenheit " + temp_range_text
    weather_descript_text = "with a " + weather_description
    atm_pressure_text = "The atmospheric pressure is " + str(current_pressure) + " Hectopascal Pressure Units "
    humidity_text = "The humidity is at " + str(current_humidity) + " percent"

    print(temp_text)
    print(weather_descript_text)
    print(atm_pressure_text)
    print(humidity_text)

    subprocess.call(['say', temp_text + weather_descript_text])
    # subprocess.call(['say', weather_descript_text])
    subprocess.call(['say', atm_pressure_text])
    subprocess.call(['say', humidity_text])


else:
    print(" City Not Found ")
