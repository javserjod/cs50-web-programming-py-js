document.addEventListener('DOMContentLoaded', function() {
    

    document.querySelectorAll('.delete-game-button').forEach(deleteButton => {
        deleteButton.addEventListener('click', deleteHandler);
    });

    
});

function deleteHandler(event){
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    event.preventDefault();
    event.stopPropagation();

    const deleteButton = event.currentTarget;
    const gameId = deleteButton.dataset.gameId;
    const recordCard = deleteButton.closest('.record-card');
    const currentPage = new URLSearchParams(window.location.search).get("page") || 1;

    console.log("Deleted game with ID:", gameId);

    fetch(`/delete_game/${gameId}?page=${currentPage}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error deleting:', data.error);
            return;
        }

        recordCard.classList.add('delete-card-effect');

         setTimeout(() => {
            const row = document.querySelector('.card-row');
            const cards = Array.from(row.children);
            const index = cards.indexOf(recordCard);
            recordCard.remove();

            // move next cards to one position before
            for (let i = index + 1; i < cards.length; i++) {
                row.children[i].before(cards[i]);
            }

            // add new card from next page, if available
            if (data.html) {
                const temp = document.createElement('div');
                temp.innerHTML = data.html.trim();
                const newCard = temp.firstChild;
                row.appendChild(newCard);
                newCard.querySelector('.delete-game-button').addEventListener('click', deleteHandler);
            }

        }, 300);
    });
};