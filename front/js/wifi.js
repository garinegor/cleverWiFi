function run(command) {
    return fetch("http://" + location.host + ":5000/run?command=" + command, {
        method: "POST"})
        .then(r => r.text());
}

function get_saved_networks(iface) {
    var r = run("wpa_cli -i wlan0 list_netowrks");
}
