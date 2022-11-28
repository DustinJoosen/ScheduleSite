document.onkeydown = function(e) {
    switch (e.code) {
        case "ArrowLeft":
            document.getElementById("set-prev-week").click();
            break;
        case "ArrowRight":
            document.getElementById("set-next-week").click();
            break;
    }
}