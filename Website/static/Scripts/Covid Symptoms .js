// JavaScript to change background color every 30 seconds
setInterval(function() {
    document.body.style.backgroundColor = "green"; // Change to desired color
    setTimeout(function() {
        document.body.style.backgroundColor = "pink"; // Change to initial color after 30 seconds
    }, 15000); // Wait for 15 seconds to revert to the initial color
}, 30000); // Repeat every 30 seconds
