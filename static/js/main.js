document.onkeydown = function(e) {
    switch (e.code) {
        case "ArrowLeft":
            document.getElementById("set-prev-week").click();
            break;
        case "ArrowRight":
            document.getElementById("set-next-week").click();
            break;
        case "KeyK":
            document.location.href = "/reload";
            break;
    }
}

// the zelfstudie checkbox is used often
const zscb = document.getElementById("zelfstudie_chkbx");

// set show_zelfstudie depending on the checkbox
zscb.onchange = function(e) {
    let value = zscb.checked;
    if (value) {
        document.cookie = "show_zelfstudie=true";
        document.location.href = "?show_zelfstudie=true";
    }
    else {
        document.cookie = "show_zelfstudie=false";
        document.location.href = "/";
    }
}

// get url info
const urlSearchParams = new URLSearchParams(window.location.search);
const params = Object.fromEntries(urlSearchParams.entries());

function get_cookie_by_name(name) {
    let match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return (match == null) ? null : match[2];
}

// modifies the url, based on the cookies
let show_zelfstudie_cookie = get_cookie_by_name("show_zelfstudie");
if (show_zelfstudie_cookie === "true") {
    // we don't want to send you to zelfstudie=true if you are already there.
    if (params.show_zelfstudie !== "true" && params.show_zelfstudie !== "yes") {
        document.location.href = "?show_zelfstudie=true";
    }

}

// set the checked attribute on the checkbox
if (params.show_zelfstudie === "true" || params.show_zelfstudie === "yes") {
    zscb.checked = true;
}

function are_cookies_allowed() {
    let cookies_allowed = get_cookie_by_name("cookies_allowed");
    if (cookies_allowed == null) {
        return false;
    }
    return cookies_allowed === "true"
}

function set_cookies_allowed(allowed) {
    let date_one_year_from_now = new Date(new Date().getTime() + 1000*3600*24*365).toGMTString();
    document.cookie = "cookies_allowed=" + allowed + "; expires=" + date_one_year_from_now;
}

if (get_cookie_by_name("cookies_allowed") == null) {
    $("#cookieModal").modal("show");
}

let selected_lesson = null;

// Not proud of this. need to refactor it.
$(".lesson").on("click", function () {
    let lesson_id = $(this).attr("content");

    // loop through all the lessons, and select the correct one based on the id.
    for (let [key, value] of Object.entries(json_schedule)) {
        for (let i = 0; i < value.length; i++) {
            if (value[i]["id"] === lesson_id) {
                selected_lesson = value[i];
            }
        }
    }
    if (selected_lesson === null) {
        return;
    }

    // Show the modal
    $("#lessonModal").modal();

    let roosterdatum = new Date(selected_lesson["roosterdatum"]);
    roosterdatum = ("0" + roosterdatum.getDate()).slice(-2) + "-" + ("0" + roosterdatum.getMonth() + 1).slice(-2) +
        "-" + roosterdatum.getFullYear();

    let roostertime_begin = new Date(selected_lesson["starttijd"]);
    roostertime_begin = ("0" + roostertime_begin.getHours()).slice(-2) + ":" +
                        ("0" + roostertime_begin.getMinutes()).slice(-2);

    let roostertime_eind = new Date(selected_lesson["eindtijd"]);
    roostertime_eind = ("0" + roostertime_eind.getHours()).slice(-2) + ":" +
                       ("0" + roostertime_eind.getMinutes()).slice(-2);

    // Add the correct info to the modal
    $("#lessonModalTitle").text(selected_lesson["leeractiviteit"]);
    $("#lessonModalDate").text(roosterdatum + " | " + roostertime_begin + " - " + roostertime_eind);
    $("#lessonModalRoom").text(selected_lesson["lokaal"]);
    $("#lessonModalClass").text(selected_lesson["groepcode"]);
    $("#lessonModalTeacher").text(selected_lesson["docentnamen"]);
    $("#lessonModalType").text(selected_lesson["type"]);
    $("#lessonModalOeEvl").text(selected_lesson["vaknaam"] + " | " + selected_lesson["vakcode"]);
    $("#lessonModalComment").text(selected_lesson["commentaar"]);
})

$(".copy-raw-data").on("click", function () {
    navigator.clipboard.writeText(JSON.stringify(selected_lesson));
    alert("lesson data copied to clipboard, in JSON format.");
})