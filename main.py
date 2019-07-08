import shlex
import logging
from flask import Flask, request
from subprocess import Popen, call, PIPE

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='commands.log',
                    filemode='w')


@app.route("/run_command", methods=["POST"])
def run_command(rcmd):
	"""
	Runs a program, and it's paramters (e.g. rcmd="ls -lh /var/www")
	Returns output if successful, or None and logs error if not.
	"""
	cmd = shlex.split(request.form["command"])
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


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)