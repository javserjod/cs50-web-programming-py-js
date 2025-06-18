document.addEventListener('DOMContentLoaded', function() {
    
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    document.querySelectorAll('.delete-game-button').forEach(deleteButton => {
        deleteButton.addEventListener('click', event => {
            event.preventDefault();
            event.stopPropagation();

            const gameId = deleteButton.dataset.gameId;
            const recordCard = deleteButton.closest('.record-card');

            console.log(recordCard);
            console.log(gameId);

            fetch(`/delete_game/${gameId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (response.ok) {
                    recordCard.classList.add('delete-card-effect');
                    setTimeout(() => recordCard.remove(), 400);
                } else {
                    console.error('Failed to delete game:', response.statusText);
                }
            })
        });
    });
});