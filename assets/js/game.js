document.addEventListener('DOMContentLoaded', function () {
    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();
    }
});
const data = window.Telegram.WebApp;

// document.addEventListener("DOMContentLoaded", function () {
//     const button = document.getElementById("click_to_coin");
//
//     button.addEventListener("click", function () {
//         if (window.Telegram && window.Telegram.WebApp) {
//             window.Telegram.WebApp.showAlert("Hello from Telegram Mini App!");
//         } else {
//             console.log("Telegram WebApp is not available");
//         }
//     });
// });
if (window.location.pathname == '/') {
    window.location.href = window.location.origin + "/" + data.initData
}

function Pform(string_) {
    return string_.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

var get_user_info = new FormData();
get_user_info.append("init_data", data.initData);
var requestOptions = {
    method: 'POST',
    body: get_user_info,
    redirect: 'follow'
};

function getUserInfo() {
    return fetch(window.location.origin + "/account/get-userInfo", requestOptions)
        .then(response => response.json())
        .catch(error => {
            console.log('error', error);
            throw error;
        });
}

getUserInfo().then(result => {

    // referrals
    document.getElementById('total_friends').innerText = result['total_referrals'];

    var user_name = document.getElementsByClassName('my_username');
    for (var i = 0; i < user_name.length; i++) {
        user_name[i].innerText = result['my_username'];
    }

    var user_coin_box = document.getElementsByClassName('coin_count');
    for (var i = 0; i < user_coin_box.length; i++) {
        user_coin_box[i].innerText = Pform(result['coin_count']);
    }

    // home
    document.getElementById('point').innerText = result['coin_count'];
    document.getElementById('pool_size').innerText = result['coin_pool'];
    document.getElementById('point_per_tap').innerText = result['coin_per_tap'];
    document.getElementById('point_can_take').innerText = result['can_take_from_pool'];

    var user_level_box = document.getElementsByClassName('user_level');
    for (var i = 0; i < user_level_box.length; i++) {
        user_level_box[i].innerText = result['level'];
    }

    document.getElementById('now_level').innerText = result['level'];
    document.getElementById('next_level').innerText = result['level'] + 1;

})


var total_point = 0;
var pool_size = 0;
var point_can_take = 0;
var point_per_tap = 1;
var fill_per_second = 1;
var user_level = 1;
var can_play = false;
var coin_earned = 0;

function reload_data_variable() {
    total_point = parseInt(document.getElementById('point').innerText);
    pool_size = parseInt(document.getElementById('pool_size').innerText);
    point_per_tap = parseInt(document.getElementById('point_per_tap').innerText);
    point_can_take = parseInt(document.getElementById('point_can_take').innerText);
    can_play = true;
    display_points(total_point, pool_size, point_can_take);

}

setTimeout(() => {
    reload_data_variable();
}, 2000);

document.getElementById('point_per_tap').innerText = point_per_tap;

let timer;
let can_send_coin_on_time = true;
document.getElementById('click_to_coin').addEventListener('mousedown', function () {

    if (can_play && point_can_take > 0) {

        total_point += point_per_tap;
        point_can_take -= point_per_tap;
        coin_earned += point_per_tap;

        display_points(total_point, pool_size, point_can_take);

        this.classList.add('shake');
        setTimeout(() => this.classList.remove('shake'), 200);

        if (can_send_coin_on_time) {
            var update_coin = new FormData();
            update_coin.append("init_data", data.initData);
            update_coin.append("coin", coin_earned);
            update_coin.append("coin_can_take", point_can_take);
            var requestOptions = {
                method: 'POST',
                body: update_coin,
                redirect: 'follow'
            };
            console.log('req send')

            function UpdateCoin() {
                return fetch(window.location.origin + "/account/update-userCoin", requestOptions)
                    .then(response => response.json())
                    .catch(error => {
                        throw error;
                    });
            }

            UpdateCoin();
            can_send_coin_on_time = false;
        }

        clearTimeout(timer);
        timer = setTimeout(() => {
            can_send_coin_on_time = true
            var update_coin = new FormData();
            update_coin.append("init_data", data.initData);
            update_coin.append("coin", coin_earned - 1);
            update_coin.append("coin_can_take", point_can_take);
            var requestOptions = {
                method: 'POST',
                body: update_coin,
                redirect: 'follow',
            };
            console.log('req send')

            function UpdateCoin() {
                return fetch(window.location.origin + "/account/update-userCoin", requestOptions)
                    .then(response => response.json())
                    .catch(error => {
                        throw error;
                    });
            }

            UpdateCoin();
            coin_earned = 0;
        }, 1500);
    }
})

function display_points(total_point, pool_size, point_can_take) {
    document.getElementById('point').innerText = Pform(total_point);
    document.getElementById('pool_size').innerText = pool_size;
    document.getElementById('point_can_take').innerText = point_can_take;
    set_size_of_bar(pool_size, point_can_take);
    set_size_of_bar_level(total_point);
}

function set_size_of_bar(pool_size, point_can_take) {
    var percent_of_bar = (point_can_take / pool_size) * 100;
    document.getElementsByClassName('progress-bar')[1].style.width = percent_of_bar + '%';
}

function set_size_of_bar_level(coins) {
    var percent_of_bar = (coins / 100000) * 100;
    document.getElementsByClassName('progress-bar')[0].style.width = percent_of_bar + '%';
}


document.getElementById('education_btn').addEventListener('click', function () {
    show_page('education', 'earn_btn')
})

document.getElementById('documentation_btn').addEventListener('click', function () {
    show_page('documentation', 'earn_btn')
})

document.getElementById('about_us_btn').addEventListener('click', function () {
    show_page('about_us', 'earn_btn')
})

var long_names = document.getElementsByClassName('hide_long_name');
for (let i = 0; i < long_names.length; i++) {
    long_names[i].innerText = hide_long_name(long_names[i].innerText);
}

function hide_long_name(name) {
    var new_name= '';
    if (name.length > 10){
        for (let i = 0; i < 10; i++) {
            new_name += name[i]
        }
        new_name += '...';
        return new_name
    }
    return name
}

