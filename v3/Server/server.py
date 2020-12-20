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
modes = ['off', 'random', 'christmas', 'study', 'party']

boards = {
    'esp8266_desk' : {'name' : 'esp8266_desk', 'mode' : modes[0], 'status' : False},
    'esp8266_bed' : {'name' : 'esp8266_bed', 'mode' : modes[0], 'status' : False}
}
serverData = {
    'modes' : modes,
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
    print('TORi/v3/Server/server: entering action(' , board, ', ', mode, ')')
    # get the board from the URL
    target_board = str(board)
    # update the board's mode
    boards[target_board]['mode'] = mode
    for i in boards:
        print(i,': ',boards[i])

    serverData = {
        'modes' : modes,
        'boards' : boards
    }

    topic = target_board + '/' + mode
    mqttc.publish(topic, target_board)
    return render_template('main.html', **serverData)

# The function below is executed when user requests all devices to update
@app.route("/<mode>/sync")
def sync(mode):
    for b in boards:
        # update the board's mode
        boards[b]['mode'] = mode

    for i in boards:
        print(i,': ',boards[i])

    serverData = {
        'modes' : modes,
        'boards' : boards
    }

    mqttc.publish(mode, "all")
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