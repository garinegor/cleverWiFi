import wifi
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

iface = wifi.get_wnics()[0]
ssids = ["Home", "F808", "Kek"]

wrap = lambda s: '\'"' + s + '"\''


@app.route("/")
def hello():
    wifi_data = {
        "pass": "somewifipassword",
        "own_name": "CLEVERWEB",
    }
    return render_template("wifi.html", wifi=wifi_data, navbar_title='network configuration')


@app.route("/wifi/available")
def available():
    ssids = [network["ssid"] for network in wifi.scan_networks("wlan0")]
    return jsonify({"available": ssids})


@app.route('/save_network', methods=['POST'])
def save_network():
    wifi.add_network(iface, {"ssid": wrap(request.form["ssid"]), "psk": wrap(request.form["psk"])})
    return redirect("/")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
