function toggleMenu() {
    document.getElementById('settings-menu').style.left = '0';
    let ad = document.getElementById('settings-ad');
    ad.style.position = 'absolute';
    ad.style.top = '56px';
    ad.style.right = '0px';
    ad.style.display = 'block';
    ad.style.background = 'none';
    ad.style.width = '100%';
    ad.onclick = function () {
        hideMenu();
    }
}

function hideMenu() {
    document.getElementById('settings-menu').style.left = '-400px';
    let ad = document.getElementById('settings-ad');
    ad.style.position = 'static';
    ad.style.top = '56px';
    ad.style.right = '0px';
    ad.style.background = '#818181';
    ad.style.width = '400px';
    ad.onclick = function () {
    }

}