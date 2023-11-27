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
function groupFunction() {
    var editForm = document.getElementById('overlay')
    if (editForm.style.display === "block") {
        editForm.style.display = "none";
    } else {
        editForm.style.display = "block";
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


$(document).ready(function() {
    $(".reply-button").click(function() {
        $(this).next(".reply-form").toggle();
    });
    $(".edit-button").click(function() {
        $(this).next(".reply-form").toggle();
    });
});
