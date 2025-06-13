document.addEventListener('DOMContentLoaded', () => {
    
    // Topic selection cards
    const topicCards = document.querySelectorAll('#topicCards .option-card');
    const hiddenInputGameTopic = document.getElementById('game-topic-hidden');

    topicCards.forEach(card => {
    card.addEventListener('click', () => {
        topicCards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        hiddenInputGameTopic.value = card.getAttribute('data-value');
    });
    });


    // Game Mode selection cards
    const modeCards = document.querySelectorAll('#gameModeCards .option-card');
    const hiddenInputGameMode = document.getElementById('game-mode-hidden');

    modeCards.forEach(card => {
    card.addEventListener('click', () => {
        modeCards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        hiddenInputGameMode.value = card.getAttribute('data-value');
    });
    });


    // Genres selection cards (fetch all genres from the server)
    async function fetchGenres() {
        const query = `query { GenreCollection }`;

        const response = await fetch("https://graphql.anilist.co", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
        });

        const result = await response.json();
        return result.data.GenreCollection;
    }

    function filterGenres(genres) {
        // remove adult genres
        filtered_genres = genres.filter(genre => genre !== "Hentai");
        return filtered_genres;
    }

    function renderGenres(genres) {
        const container = document.getElementById("genreCards");
        const controlContainer = document.getElementById("genreControls");
        const hiddenInput = document.getElementById("game-genres-hidden");
        const loadingSpinner = document.getElementById("loadingSpinner");
        let selected = new Set();
        
        function triggerClickEffect(card) {
            card.classList.add("clicked");
            setTimeout(() => card.classList.remove("clicked"), 400);
        }

        // hide spinner
        loadingSpinner.style.display = "none";
        
        const updateHiddenInput = () => {
            hiddenInput.value = Array.from(selected).join(",");
        };

        // select all genres card
        const selectAllCard = document.createElement("div");
        selectAllCard.className = "control-card";
        selectAllCard.textContent = "Select All";

        selectAllCard.addEventListener("click", () => {
            const genreCards = document.querySelectorAll(".genre-card");
            genreCards.forEach(card => {
                card.classList.add("selected");
                selected.add(card.dataset.value);
            });
            updateHiddenInput();
            triggerClickEffect(selectAllCard);
        });
        controlContainer.appendChild(selectAllCard);

        // deselect all genres card
        const unselectAllCard = document.createElement("div");
        unselectAllCard.className = "control-card";
        unselectAllCard.textContent = "Unselect All";
        unselectAllCard.addEventListener("click", () => {
            const genreCards = document.querySelectorAll(".genre-card");
            genreCards.forEach(card => {
                card.classList.remove("selected");
            });
            selected.clear();
            updateHiddenInput();
            triggerClickEffect(unselectAllCard);
        });
        controlContainer.appendChild(unselectAllCard);


        // show cards fetched from the server
        genres.forEach((genre) => {
            const card = document.createElement("div");
            card.className = "option-card genre-card selected";  // selected by default
            card.textContent = genre;
            card.dataset.value = genre;

            card.addEventListener("click", () => {

                card.classList.toggle("selected");
                if (selected.has(genre)) {
                selected.delete(genre);
                } else {
                selected.add(genre);
                }
                hiddenInput.value = Array.from(selected).join(",");
            });

            container.appendChild(card);
        });
        
    }

    fetchGenres()
    /* update hidden input with all genres by default */
    .then(genres => {
        genres = filterGenres(genres);
        const hiddenInput = document.getElementById("game-genres-hidden");
        hiddenInput.value = genres.join(",");
        return genres;
    })
    .then(renderGenres)
    .catch(() => {
        document.getElementById("loadingSpinner").innerHTML = '<div class="alert alert-danger" role="alert">Failed to load genres. Please try again later.</div>';
        });
});
