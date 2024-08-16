document.addEventListener('DOMContentLoaded', function () {
    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();
    }
});
const data = window.Telegram.WebApp;

document.getElementById('home_btn').href = window.location.origin + "/home/" + data.initData;
document.getElementById('improve_btn').href = window.location.origin + "/improve/" + data.initData;
document.getElementById('investment_btn').href = window.location.origin + "/invest/" + data.initData;