// document.addEventListener('DOMContentLoaded', function () {
//     if (window.Telegram && window.Telegram.WebApp) {
//         window.Telegram.WebApp.ready();
//         window.Telegram.WebApp.expand();
//     }
// });
// const data = window.Telegram.WebApp;
//
// var get_user_info = new FormData();
// get_user_info.append("init_data", data.initData);
// var requestOptions = {
//     method: 'POST',
//     body: get_user_info,
//     redirect: 'follow'
// };
//
// function getUserInfo() {
//     return fetch(window.location.origin + "/account/get-userInfo", requestOptions)
//         .then(response => response.json())
//         .catch(error => {
//             console.log('error', error);
//             throw error;
//         });
// }
// getUserInfo().then(result => {
//     // Use the result her
//     console.log(result);
//     // You can also assign it to a variable or pass it to another function
// })





