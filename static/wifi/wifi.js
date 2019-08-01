refresh();

function refresh() {
    var req = new XMLHttpRequest();
    req.open("GET", "/wifi/available", false);
    req.send();
    if (req.status !== 200) {
        refresh();
    } else {
        var wifis = JSON.parse(req.responseText).available;
        document.getElementById("inputSSID").innerHTML = "";
        for (let i = 0; i < wifis.length; i++) {
            document.getElementById("inputSSID").innerHTML += "<option>" + wifis[i] + "</option>";
        }
    }
}

function swap(b) {
    if (b) {
        document.getElementById('title').innerText = 'AP';
        document.getElementById('title').style.color = '#17a2b8';
        document.getElementById('ssid_content').innerHTML = '<input onchange="kek()" id="inputSSID" type="text" class="form-control" aria-describedby="ssidHelp"\n' +
            'value="' + own_net_name + '" placeholder="SSID">';
        document.getElementById('ssidHelp2').innerText = 'Your Clever WiFi hotspot configuration';
        document.getElementById('butt_ref').innerText = 'Client mode';
        document.getElementById('butt_save').innerText = 'Turn on';
        document.getElementById("butt_save").classList.remove('btn-success');
        document.getElementById("butt_save").classList.add('btn-info');
        document.getElementById('butt_save').onclick = function () {
            save();
        }
    } else {
        document.getElementById('title').innerText = 'Client';
        document.getElementById('title').style.color = '#28a745';
        document.getElementById('ssid_content').innerHTML = '<select id="inputSSID" class="form-control"></select>';
        document.getElementById('ssidHelp2').innerText = 'WiFi hotspot configuration that Clever can connect';
        refresh();
        document.getElementById("butt_save").classList.add('btn-success');
        document.getElementById("butt_save").classList.remove('btn-info');
        document.getElementById('butt_ref').innerText = 'AP mode';
        document.getElementById('butt_save').innerText = 'Connect';
        document.getElementById('butt_save').onclick = function () {
            connect();
        };
    }
    document.getElementById('butt_ref').onclick = function () {
        swap(!b);
    };
}

function kek() {
    own_net_name = document.getElementById("inputSSID").value;
}

function hidePassword() {
    document.getElementById('password').type = "password";
    document.getElementById('password-toggler').onclick = function () {
        showPassword();
    };
    document.getElementById('toggler-icon').src = vis_image_url;
}

function showPassword() {
    document.getElementById('password').type = "text";
    document.getElementById('password-toggler').onclick = function () {
        hidePassword();
    };
    document.getElementById('toggler-icon').src = invis_image_url;
}

//For Egor

function connect() {
    let ssid = document.getElementById('inputSSID').value;
    let psk = document.getElementById('password').value;

    fetch("http://" + location.host + "/network/add", {
        method: "POST",
        headers:
            {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({ parameters: { ssid: ssid, psk: psk } })
    })
        .then(r => { console.log(r) });

    console.log('Connect', ssid, psk);
}

function save() {
    let ssid = document.getElementById('inputSSID').value;
    let password = document.getElementById('password').value;
    console.log('Save', ssid, password);
}