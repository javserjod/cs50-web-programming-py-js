document.addEventListener('DOMContentLoaded', function() {

    const csrftoken = document.querySelector('meta[name="csrf-token"]').content;

    // Edit Button
    document.querySelectorAll('.edit').forEach(editButton => {
        editButton.addEventListener('click', event => {
            const element = event.target;
            const postDiv = element.closest('.post');
            let contentDiv = postDiv.querySelector('.content');
            console.log("ContentDiv", element.closest('.post'));

            const postId = postDiv.dataset.postId;
            const firstChild = contentDiv.firstElementChild;

            console.log("Edit button clicked", firstChild.tagName);
            if (firstChild.tagName == 'P') {
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

                    console.log(postId, newContent)
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
            }
        });
    });

    // Delete Button
    deleteButton = document.querySelector('.delete')
    deleteButton.addEventListener('click', function() {
        console.log("Delete clicked");
    })
})