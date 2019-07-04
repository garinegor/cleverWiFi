import wifi
from flask import Flask, render_template

app = Flask(__name__)

ssids = ["Home", "F808", "Kek"]


@app.route("/")
def hello():
	ssids = [network["ssid"] for network in wifi.scan_networks("wlan0")]
	return render_template("wifi.html", ssids=ssids)


@app.route('/save_network', methods=['POST'])
def save_network(request):
	wifi.add_network("wlan0", {"ssid": request.ssid, "psk": request.psk})

