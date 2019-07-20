import shlex
import logging
from flask import Flask, request
from flask_cors import CORS
from subprocess import Popen, call, PIPE

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='commands.log',
                    filemode='w')

app = Flask(__name__)
CORS(app)


@app.route("/run", methods=["POST"])
def run_command():
	"""
	Runs a program, and it's paramters (e.g. rcmd="ls -lh /var/www")
	Returns output if successful, or None and logs error if not.
	"""
	print request.values
	cmd = shlex.split(request.args["command"])
	executable = cmd[0]
	executable_options = cmd[1:]
	response_stdout = ""


	try:
		proc = Popen(([executable] + executable_options), stdout=PIPE, stderr=PIPE)
		response = proc.communicate()
		response_stdout, response_stderr = response[0], response[1]
	except OSError, e:
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


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
