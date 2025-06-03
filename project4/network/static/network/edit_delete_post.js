document.addEventListener('DOMContentLoaded', function() {

    const csrftoken = document.querySelector('meta[name="csrf-token"]').content;

    function cancelAllEdits() {
        // Cancel all edits by reverting all forms to p
        document.querySelectorAll('.post').forEach(postDiv => {
            const contentDiv = postDiv.querySelector('.content');
            const form = contentDiv.querySelector('form');
            if (form) {
                // if form, change to p
                const originalContent = form.querySelector('textarea')?.defaultValue || '';
                contentDiv.innerHTML = `<p>${originalContent}</p>`;
            }
        });
    }

    // Edit Button
    document.querySelectorAll('.edit').forEach(editButton => {
        editButton.addEventListener('click', event => {
            const element = event.currentTarget;    // edit button 
            const postDiv = element.closest('.post');   // whole post div
            const contentDiv = postDiv.querySelector('.content');   // content div
            const postId = postDiv.dataset.postId;   // current post id
            const firstChild = contentDiv.firstElementChild;    // p inside content div

            console.log(`Edit button clicked. Post #${postId}`);
            
            if (firstChild.tagName == 'P') {
                const originalContent = firstChild.innerHTML;   // text inside p
                
                cancelAllEdits();
                
                // Change UI to show the edit form
                contentDiv.innerHTML = `<form action="/network/edit_post" method="post">
                    <textarea name="content" id="content-textarea" class="form-control mb-3" style="min-height:50px;" required>${firstChild.innerHTML}</textarea>
                    <input type="hidden" name="post_id" value="${postId}">
                    <div class="d-flex justify-content-between mb-3">
                        <button type="submit" class="save-edit btn btn-primary">Save</button>
                        <button type="button" class="cancel-edit btn btn-secondary">Cancel Edit</button>
                    </div>
                </form>`;

                saveButton = contentDiv.querySelector('.save-edit');
                saveButton.addEventListener('click', function(event) {
                    console.log("Save button clicked");
                    event.preventDefault();
                    newContent = document.querySelector('#content-textarea').value
                    // Change UI to show the updated content
                    contentDiv.innerHTML = `<p>${newContent}</p>`;

                    // Update the post content in the backend
                    fetch('/edit_post', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                        body: JSON.stringify({
                            post_id: postId,
                            content: newContent
                        })
                    })
                });

                cancelButton = contentDiv.querySelector('.cancel-edit');
                cancelButton.addEventListener('click', function(event) {
                    console.log(`Cancel Edit button clicked. Post #${postId}`);
                    event.preventDefault();
                    contentDiv.innerHTML = `<p>${originalContent}</p>`;
                });
            }
        });
    });

    // Delete Button
    document.querySelectorAll('.delete').forEach(deleteButton => {
        deleteButton.addEventListener('click', event => {
            const element = event.currentTarget;    // delete button
            const postDiv = element.closest('.post');   // whole post div
            const postId = postDiv.dataset.postId;   // current post id
            
            console.log(`Delete button clicked. Post #${postId}`);
            
            // Change UI to remove the post
            postDiv.remove();  // Remove the post from the DOM
            console.log(`Post #${postId} deleted from UI`);
            
            // Send a request to delete the post from the backend
            fetch("/delete_post", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ post_id: postId })
            });
        });
    });

});