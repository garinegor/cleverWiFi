function run(command) {
    return fetch("http://" + location.host + ":5000/run?command=" + command, {
        method: "POST"})
        .then(r => r.text());
}

function get_saved_networks(iface) {
    var networks = {};

    var command = "wpa_cli -i " + iface +  " list_netowrks";
    var r = run(command)
        .then(function (response) {
            if (response.split("\n").length > 1) {
                response.split("\n").slice(1, -1).forEach(function (line) {
                    var parameters = line.split("\t");
                    networks[parseInt(parameters[0])] = parameters[1];
                });
            }
        });

    return networks;
}
