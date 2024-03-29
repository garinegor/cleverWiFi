#!/usr/bin/env python
# # -*- coding: utf-8 -*-
from subprocess import Popen, call, PIPE
import errno
from types import *
import logging
import sys
import logging
import time
import argparse
import shlex

SUPPLICANT_LOG_FILE = "wpa_supplicant.log"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='wifi.log',
                    filemode='w')


def add_network(_iface, _parameters):
	"""
	Add new network with passed parameters to the end of the networks list. Disables all other networks
	"""
	id = run_program("wpa_cli -i %s add_network")[:-1]
	if id.isdigit():
		for parameter in _parameters:
			_set_parameter(_iface, id, parameter, _parameters[parameter])
		enable_network(id)
		return id
	else:
		logging.error("Unable to add new network.")
		return None


def select_network(_iface, _id):
	"""
	Set the highest prioriry to the network with passed id
	"""
	r = run_program("wpa_cli -i %s list_networks" % _iface)
	ids = list(map(int, [i.split()[0] for i in r.split("\n")[1: -1]]))
	priorities = list(map(int, [_get_parameter(_iface, id, "priority") for id in ids]))
	present_index = ids.index(id)
	target_index = priorities.index(max(priorities))
	if target_index != present_index:
		_set_parameter(_iface, ids[present_index], "priority", priorities[target_index])
		_set_parameter(_iface, ids[target_index], "priority", priorities[present_index])


def scan_networks(_iface, retry=10):
	"""
	Grab a list of wireless networks within range, and return a list of dicts describing them.
	"""
	while retry > 0:
		if "OK" in run_program("wpa_cli -i %s scan" % _iface):
			networks = []
			r = run_program("wpa_cli -i %s scan_result" % _iface).strip()
			if "bssid" in r and len(r.split("\n")) > 1:
				for line in r.split("\n")[1:]:
					b, fr, s, f = line.split()[:4]
					ss = " ".join(line.split()[4:])  # Hmm, dirty
					networks.append({"bssid": b, "freq": fr, "sig": s, "ssid": ss, "flag": f})
				return networks
		retry -= 1
		logging.debug("Couldn't retrieve networks, retrying")
		time.sleep(0.5)
	logging.error("Failed to list networks")


def get_saved_networks(_iface):
	"""
	Get list with networks saved in wpa_supplicant
	"""
	r = run_program("wpa_cli -i %s list_networks" % _iface)
	networks = []
	if len(r.split("\n")) > 1:
		for network in r.split("\n")[1:-1]:
			parameters = network.split()
			nid = int(parameters[0])
			networks.append(dict(zip(["id", "ssid", "mode"], [nid, parameters[1], int(_get_parameter(_iface, nid, "mode"))])))
	return networks


def switch_mode(_mode):
	"""
	Configure static IP and services
	"""
	if _mode == "cli":
		run_program("")
		run_program("")
		run_program("")
		run_program("")
		run_program("")
		run_program("")
	elif _mode == "ap":
		with open("/etc/dhcpcd.conf", "a") as f:
			f.write("")
		run_program("")
		run_program("")
		run_program("")
		run_program("")
		run_program("")


def enable_network(_iface, _id):
	"""
	Enable network with passed id
	"""
	run_program("wpa_cli -i %s enable_network %d" % (_iface,  _id))


def disable_network(_iface, _id):
	"""
	Disable network with passed id
	"""
	run_program("wpa_cli -i %s disable_network %d" % (_iface,  _id))


def _get_parameter(_iface, _id, _name):
	"""
	Get network parameter value
	"""
	return run_program("wpa_cli -i %s get_network %d %s" % (_iface, _id, _name))


def _set_parameter(_iface, _id, _name, _value):
	"""
	Set network parameter value
	"""
	return run_program("wpa_cli -i %s set_network %d %s %s" % (_iface, _id, _name, _value))


def run_program(rcmd):
	"""
	Runs a program, and it's paramters (e.g. rcmd="ls -lh /var/www")
	Returns output if successful, or None and logs error if not.
	"""

	cmd = shlex.split(rcmd)
	executable = cmd[0]
	executable_options = cmd[1:]

	try:
		proc = Popen(([executable] + executable_options), stdout=PIPE, stderr=PIPE)
		response = proc.communicate()
		response_stdout, response_stderr = response[0], response[1]
	except OSError, e:
		if e.errno == errno.ENOENT:
			logging.debug("Unable to locate '%s' program. Is it in your path?" % executable)
		else:
			logging.error("O/S error occured when trying to run '%s': \"%s\"" % (executable, str(e)))
	except ValueError, e:
		logging.debug("Value error occured. Check your parameters.")
	else:
		if proc.wait() != 0:
			logging.debug("Executable '%s' returned with the error: \"%s\"" % (executable, response_stderr))
			return response
		else:
			logging.debug("Executable '%s' returned successfully. First line of response was \"%s\"" % (
			executable, response_stdout.split('\n')[0]))
			return response_stdout


def start_wpa(_iface):
	"""
	Terminates any running wpa_supplicant process, and then starts a new one.
	"""
	run_program("wpa_cli terminate")
	time.sleep(1)
	run_program("wpa_supplicant -B -Dwext -i %s -C /var/run/wpa_supplicant -f %s" % (_iface, SUPPLICANT_LOG_FILE))


def get_wnics():
	"""
	Kludgey way to get wireless NICs, not sure if cross platform.
	"""
	r = run_program("iwconfig")
	ifaces = []
	for line in r.split("\n"):
		if "IEEE" in line:
			ifaces.append(line.split()[0])
	return ifaces

