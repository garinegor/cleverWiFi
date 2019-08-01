import wifi
from flask import Flask, render_template, request, redirect, jsonify, make_response

response_template = {"data": {}}

app = Flask(__name__)

iface = wifi.get_wnics()[0]
ssids = ["Home", "F808", "Kek"]

wrap = lambda s: '\'"' + s + '"\''


@app.route("/")
@app.route("/settings")
def settings():
    settings_menu = [
        {
            'title': 'WiFi',
            'content': [
                {'title': 'Configuration', 'template': 'wifi_config.html'}
            ]
        }
    ]



    wifi_data = {
        "pass": "somewifipassword",
        "own_name": "CLEVERWEB",
        "is_ap": False
    }

    return render_template("settings.html", wifi=wifi_data, navbar_title='settings', settings=settings_menu)


@app.route("/wifi/available")
def available_networks():
    ssids = [network["ssid"] for network in wifi.scan_networks("wlan0")]
    return jsonify({"available": ssids})


@app.route("/network/add", methods=["POST"])
def add_network():
    """
    Save new network and return it's ID
    """
    response = response_template

    parameters = request.get_json()["parameters"]
    # parameters = zip(parameters.keys(), list(map(wrap, parameters.values())))

    new_network = wifi.add_network(iface, parameters)
    if new_network:
        response["data"] = {"network_id": new_network}
        response = make_response(jsonify(response), 200)
    else:
        response["error"] = "failed to add new network"
        response = make_response(jsonify(response), 500)

    return response


@app.route("/network/select", methods=["POST"])
def select_network():
    """
    Select network with specified ID
    """
    wifi.select_network(iface, id)
    return response_template


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
