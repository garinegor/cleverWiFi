def swap_content(file1, file2):
  with open(file1, "r") as f1:
		f1_content = f1.readlines()

	with open(file1, "w+") as f1:
		with open(file2, "r") as f2:
			for line in f2.readlines():
				f1.write(line)

		with open(file2, "w+") as f2:
			for line in f1_content:
				f2.write(line)


swap_content("1.txt", "2.txt")


# matches = [re.search(network_name_regex, match.group()).group()[6:-1] for match in re.finditer(network_conf_regex, conf) if not "mode=2" in match.group()]


import re, os

PATH_TO_WPA_CONF = "/etc/wpa_supplicant/wpa_supplicant.conf"
PATH_TO_DNS_CONF = "/etc/dhcpcd.conf"

PATH_TO_BUFFER_CONF = "confs/buff.conf"


network_conf_regex = r'network=\{((?!#).|\n)*?\}'



def save_new_net(cli_conf_file, ssid, psk):
	with open(cli_conf_file, "a") as f:
		network = 'network={\n    ssid="%s"\n    psk="%s"\n}' % (ssid, psk)
		f.write(network)


def change_saved_net_psk(cli_conf_file, ssid, psk):
	# change saved network password
	with open(cli_conf_file) as f:
		configuration = f.read()
		for network_match in re.finditer(network_conf_regex, configuration):
			network = network_match.group()
			if 'ssid="%s"' % ssid in network:
				network = change_value(network, "psk", psk)
				with open(cli_conf_file, "w") as f1:
					f1.write(configuration[:network_match.start()] + network + configuration[network_match.end():])
				return True
		return False


def scan_nets():
	pass
	# scan for networks with wifi library
	# check for saved available nets
	# return dict with ssid: pwd to fill page fields


def get_saved_nets(cli_conf_file):
	# returns all networks, saved in wpa_supplicant
	with open(cli_conf_file) as f:
		conf = f.read()
		networks = []
		for network_match in re.finditer(network_conf_regex, conf):
			if "mode=2" not in network_match.group():
				networks.append(re.search(network_name_regex, network_match.group()).group()[6:-1])

		return networks if networks else None


def set_ap_conf(ap_conf_file, ssid, psk):
	# wpa_supplicant ssid and pwd edit
	with open(ap_conf_file) as f:
		configuration = f.read()

		for network_match in re.finditer(network_conf_regex, configuration):
			network = network_match.group()

			if "mode=2" in network:
				network = change_value(network, "ssid", ssid)
				network = change_value(network, "psk", psk)

				with open(ap_conf_file, "w") as f1:
					f1.write(configuration[:network_match.start()] + network + configuration[network_match.end():])

				return True

		return False


def get_ap_conf():
	pass


def set_mode(mode):
	if mode == "cli":
		print "client mode"

		# dnsmasq disable
		os.system("sudo systemctl stop dnsmasq")
		os.system("sudo systemctl disable dnsmasq")

		# conf file edit
		os.system("sudo sed -i 's/interface wlan0//' /etc/dhcpcd.conf")
		os.system("sudo sed -i 's/static ip_address=192.168.11.1\/24//' /etc/dhcpcd.conf")

		# swap ap and cli mode confs
#		swap_file_content(PATH_TO_WPA_CONF, PATH_TO_BUFFER_CONF)

		# restart dhcpcd
		os.system("sudo systemctl restart dhcpcd")

	elif mode == "ap":
		print "ap mode"

		# add dnsmasq ap configuration
		with open(PATH_TO_DNS_CONF, "a") as f:
			f.write("\ninterface wlan0")
			f.write("\nstatic ip_address=192.168.11.1/24")

		# swap cli and ap mode confs
		swap_file_content(PATH_TO_WPA_CONF, PATH_TO_BUFFER_CONF)

		# ap mode commands
		os.system("sudo systemctl daemon-reload")
		os.system("sudo systemctl enable dnsmasq")
		os.system("sudo systemctl start dnsmasq")
		os.system("sudo systemctl restart dhcpcd")


def get_mode():
	with open(PATH_TO_DNS_CONF, "r") as f:
		return "ap" if "static ip_address=" in f.read() else "cli"


def swap_file_content(file1, file2):
	with open(file1, "r") as f1:
		f1_content = f1.readlines()

	with open(file1, "w+") as f1:
		with open(file2, "r") as f2:
			for line in f2.readlines():
				f1.write(line)

		with open(file2, "w+") as f2:
			for line in f1_content:
				f2.write(line)


def change_value(network, key, value):
	key_regex = r'%s=\"(\w|[ _-])*\"' % key
	key_match = re.search(key_regex, network)
	network = network[:key_match.start() + len(key) + 2] + value + network[key_match.end() - 1 :]
	return network
