# source: https://randomnerdtutorials.com/raspberry-pi-publishing-mqtt-messages-to-esp8266/

# order of execution:
# 1. call start(app) -> begins the server
# 2. main() is called to initialize the webpage
# 3. action() is called when webpage is redirected (action was taken)

import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
app = Flask(__name__)

mqttc = mqtt.Client()
mqttc.connect("localhost", 1883, 60)
mqttc.loop_start()

# dictionary of client devices
# 'mode' corresponds to the mode each board is running
# 'status' indicates whether or not the board is connected to the server

boards = {
    'esp8266_door' : {
        'name' : 'esp8266_door', 
        'option' : 'on', 
    },
    'esp8266_desk' : {
        'name' : 'esp8266_desk', 
        'mode' : 'off', 
        'rgb' : {
            'red' : 0, 
            'green' : 0, 
            'blue' : 0
        }
    },
    'esp8266_bed' : {
        'name' : 'esp8266_bed', 
        'mode' : 'off', 
        'rgb' : {
            'red' : 0, 
            'green' : 0, 
            'blue' : 0
        }
    },
    'esp8266_rclambo' : {
        'name' : 'esp8266_rclambo', 
        'mode' : 'off', 
        'rgb' : {
            'red' : 0, 
            'green' : 0, 
            'blue' : 0
        }
    }
}
serverData = {
    'boards' : boards
}

# called to start the server
def server_start():
    app.run(host='0.0.0.0', port=8181, debug=True)
    return app

@app.route("/") # determines what URL should trigger the function
def main():
    print('TORi/v3/Server/server: entering main()')
    # Pass the server data into the template main.html and return it to the user
    return render_template('main.html', **serverData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<board>/<mode>")
def action(board, mode):
    print('Entering action(' , board, ', ', mode, ')')
    # get the board from the URL
    target_board = str(board)
    # update the board's mode
    boards[target_board]['mode'] = mode
    for i in boards:
        print(i,': ',boards[i])

    serverData = {
        'boards' : boards
    }

    topic = target_board + '/' + mode
    mqttc.publish(topic, target_board) # publish() takes topic and message as parameters
    return render_template('main.html', **serverData)

# The function below is executed when user requests all devices to update
@app.route("/<mode>/sync")
def sync(mode):
    print('Entering sync(',mode,')')
    for b in boards:
        if b != 'esp8266_door':
            # update the board's mode
            boards[b]['mode'] = mode

    for i in boards:
        print(i,': ',boards[i])

    serverData = {
        'boards' : boards
    }

    mqttc.publish(mode, "all")
    return render_template('main.html', **serverData)


@app.route("/<mode>/sync/<red>/<green>/<blue>")
def syncRGB(mode, red, green, blue):
    print('Entering syncRGB(', mode, ',', red, ',', green, ',', blue, ')')
    for b in boards:
        if b != 'esp8266_door':
            # update the board's mode
            boards[b]['mode'] = mode
            boards[b]['rgb']['red'] = int(red)
            boards[b]['rgb']['green'] = int(green)
            boards[b]['rgb']['blue'] = int(blue)

    for i in boards:
        print(i,': ',boards[i])

    serverData = {
        'boards' : boards
    }

    message = red + '/' + green + '/' + blue
    mqttc.publish("all/rgb", message)
    return render_template('main.html', **serverData)

# this funciton is executed when the RGB sliders are used in the Flutter application
@app.route("/<board>/<mode>/<red>/<green>/<blue>")
def rgb(board, mode, red, green, blue):
     print('Entering rgb(',red,',',green,',',blue,')')
     target_board = str(board)
     boards[target_board]['mode'] = mode
     boards[target_board]['rgb']['red'] = int(red)
     boards[target_board]['rgb']['green'] = int(green)
     boards[target_board]['rgb']['blue'] = int(blue)

     serverData = {
        'boards' : boards
    }
     
     topic = target_board + '/rgb'
     message = red + '/' + green + '/' + blue
     mqttc.publish(topic, message)
     return render_template('main.html', **serverData)

@app.route("/esp8266_door/<option>")
def doorOption(option):
    if option == 'toggle':
        # switch to opposite state
        if boards['esp8266_door']['option'] == 'on':
            boards['esp8266_door']['option'] = 'off'
        elif boards['esp8266_door']['option'] == 'off':
            boards['esp8266_door']['option'] = 'on'
    # set back to 'on'
    elif option == 'reset':
        boards['esp8266_door']['option'] = 'on'
    # set to 'keep_on' or 'keep_off'
    else:
        boards['esp8266_door']['option'] = option

    serverData = {
        'boards' : boards
    }

    topic = 'esp8266_door'
    message = option
    mqttc.publish(topic, message)
    return render_template('main.html', **serverData)
    


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'