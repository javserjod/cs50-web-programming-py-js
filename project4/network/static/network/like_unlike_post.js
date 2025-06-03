document.addEventListener('DOMContentLoaded', function() {

    const csrftoken = document.querySelector('meta[name="csrf-token"]').content;

    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const likeButton = event.currentTarget; // like button
            const postDiv = likeButton.closest('.post');  
            const postId = postDiv.dataset.postId;
            let likeCount = parseInt(likeButton.dataset.postLikeCount);

            if (!likeButton.classList.contains('liked')) {
                // if post not liked, add like
                // Change UI to show the post is liked
                likeCount++;
                likeButton.classList = 'like-button btn btn-danger border liked';  // Add the 'liked' class to the button and style it accordingly
                console.log(`Like post #${postId}`);	
                likeButton.innerHTML = `<i class="bi bi-suit-heart-fill"></i> ${likeCount}`;
                likeButton.dataset.postLikeCount = likeCount;  // Update the like count in the button's data attribute
                // Backend request to like the post
                fetch('/like_post', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ post_id: postId })
                })
            } else {
                // if post already liked, remove like
                // Change UI to show the post is unliked
                likeCount--;
                likeButton.classList = "like-button btn btn-secondary border";  // Remove the 'liked' class and set appropriate style
                console.log(`Unlike post #${postId}`);	
                likeButton.innerHTML = `<i class="bi bi-suit-heart"></i> ${likeCount}`;
                likeButton.dataset.postLikeCount = likeCount;  // Update the like count in the button's data attribute
                // Backend request to unlike the post
                fetch('/unlike_post', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ post_id: postId })
                })
            }
        });
    });
});