window.addEventListener('load', function () {
    setTimeout(function () {
        document.getElementById('footer_load').hidden = false;
        document.getElementById('loading_page').hidden = true;
        show_page('home', 'home_btn');
    }, 1000);
})

function disableScroll() {
    scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    scrollLeft = window.pageXOffset || document.documentElement.scrollLeft, window.onscroll = function () {
        window.scrollTo(scrollLeft, scrollTop);
    };
}


function show_page(page_name, active_btn) {
    var pages_name_in_list = ['home', 'improve', 'investment', 'friends', 'players', 'guide', 'education', 'about_us', 'documentation']
    for (var i = 0; i < pages_name_in_list.length; i++) {
        document.getElementById(pages_name_in_list[i]).hidden = true;
    }
    document.getElementById(page_name).hidden = false;


    var btn_name_in_list = ['home_btn', 'improve_btn', 'friend_btn', 'investment_btn']
    for (var i = 0; i < btn_name_in_list.length; i++) {
        try {
            document.getElementById(btn_name_in_list[i]).classList.remove("active");
        } catch (e) {
        }
    }
    try {
        document.getElementById(active_btn).classList.add("active");
    } catch (e) {
    }


}

document.getElementsByClassName('plinko-loading-spinner')[0].style.left = window.innerWidth / 2 + "px";

document.getElementById('copy_ref_link_btn').addEventListener('click', function () {
    const ref_link = JSON.parse(document.getElementById('ref_link').textContent);
    navigator.clipboard.writeText(ref_link)
})







