function toggleMenu() {
    const menu = document.querySelector(".fab-menu");
    menu.style.display = (menu.style.display === "block") ? "none" : "block";
}

function menuAction(option) {
    alert("You selected: " + option);
    openOverlay()
    toggleMenu()
}

function openOverlay() {
    document.getElementById("overlay").style.display = "flex";
    toggleMenu()
}

function closeOverlay() {
    document.getElementById("overlay").style.display = "none";
}