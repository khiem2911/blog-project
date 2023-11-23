function myFunction(postId) {
    var dropdown = document.getElementById("myDropdown-" + postId);
    dropdown.classList.toggle("show");

    var editForm = document.getElementById("edit-form-" + postId);
    if (editForm.style.display === "block") {
        editForm.style.display = "none";
    } else {
        editForm.style.display = "block";
    }
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}


document.querySelectorAll(".edit-link").forEach(function(link) {
    link.addEventListener("click", function(e) {
        e.preventDefault(); // Prevent the default link behavior (navigation)

        var postId = this.getAttribute("data-post-id");
        var overlay = document.querySelector(".overlay[data-post-id='" + postId + "']");
        overlay.style.display = "block";
    });
});

// Add event listeners to all close buttons
document.querySelectorAll(".close-overlay").forEach(function(button) {
    button.addEventListener("click", function() {
        var overlay = this.closest(".overlay");
        overlay.style.display = "none";
    });
});
// Comments
$(document).ready(function() {
    $(".reply-button").click(function() {
        $(this).next(".reply-form").toggle();
    });
    $(".edit-button").click(function() {
        $(this).next(".reply-form").toggle();
    });
});

// Create post
setTimeout(function() {
    var messages = document.querySelectorAll('.custom-alert');
    for (var i = 0; i < messages.length; i++) {
        messages[i].style.display = 'none';
    }
}, 5000); 