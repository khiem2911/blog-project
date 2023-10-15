function showMoreComments(event) {
    event.preventDefault();
    event.target.style.display = 'none';
    
    var commentsContainer = event.target.previousElementSibling;
    var hiddenComments = commentsContainer.getElementsByClassName('hide-comments');
    for (var i = 0; i < hiddenComments.length && i < 10; i++) {
        hiddenComments[i].classList.remove('hide-comments');
    }
}