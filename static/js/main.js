document.onkeydown = function(e) {
    switch (e.code) {
        case "ArrowLeft":
            document.getElementById("set-prev-week").click();
            break;
        case "ArrowRight":
            document.getElementById("set-next-week").click();
            break;
        // case "ArrowUp":
        // case "ArrowDown":
        //     document.getElementById("set-curr-week").click();
        //     break;
        case "Escape":
            document.getElementById("greyed_main").style.display = "none";
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

// modifies the url, based on the cookies
let match = document.cookie.match(new RegExp('(^| )' + "show_zelfstudie" + '=([^;]+)'));
if (match) {
    if (match[2] === "true") {
        // we don't want to send you to zelfstudie=true if you are already there.
        if (params.show_zelfstudie !== "true" && params.show_zelfstudie !== "yes") {
            document.location.href = "?show_zelfstudie=true";
        }
    }
}

// set the checked attribute on the checkbox
if (params.show_zelfstudie === "true" || params.show_zelfstudie === "yes") {
    zscb.checked = true;
}


$(".lesson").on("click", function () {
    $("#greyed_main").css("display", "block");
});

$("#back_to_schedule").on("click", function () {
    $("#greyed_main").toggle();
})

$("#copy_raw_data").on("click", function () {
    alert("Raw JSON data is now copied to clipboard");
    navigator.clipboard.writeText("Deze functionaliteit is nog niet af.");
});
