document.addEventListener('DOMContentLoaded', () => {
    const inputCover = document.getElementById("guessCoverInput");
    const inputCharacter = document.getElementById("guessCharacterInput");
    const suggestionBox = document.getElementById("suggestions");

    let timeout = null;

    const N_RESULTS_PER_PAGE = 10; // Number of results per page for suggestions


    // Character Image Gamemode ------------------------------
    if (inputCharacter) {

        inputCharacter.addEventListener("input", () => {
            const queryText = inputCharacter.value.trim();

            // Cancel previous timer to avoid spam
            clearTimeout(timeout);

            if (queryText.length < 1) {
                suggestionBox.innerHTML = "";
                return;
            }

            timeout = setTimeout(() => {
                fetchSuggestionsCharacters(queryText);
            }, 500); // delay to avoid calling on every keystroke
        });

        async function fetchSuggestionsCharacters(search) {
            const query = `
            query ($search: String, $perPage: Int) {
                Page(perPage: $perPage) {
                    characters(search: $search) {
                        id
                        name { full }
                        media(sort: POPULARITY_DESC) {
                            nodes {
                                title {
                                    romaji
                                }
                            }
                        }
                    }
                }
            }`;

            const variables = { 
                search, 
                "perPage": N_RESULTS_PER_PAGE
            };

            try {
                const res = await fetch("https://graphql.anilist.co", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query, variables })
                });

                const data = await res.json();
                const characters = data.data.Page.characters;

                /* check if the search term is empty */
                const filtered = characters.filter(char =>
                    char.name.full.toLowerCase().includes(search.toLowerCase())
                );

                const results = filtered.length > 0 ? filtered : null;

                if (results === null) {
                    suggestionBox.innerHTML = "<div class='text-muted px-2 py-1' style='cursor: pointer;'>No results found</div>";
                    return;
                }
                else {
                    suggestionBox.innerHTML = "";
                    results.forEach(char => {
                        const item = document.createElement("div");
                        item.className = "p-2 suggestion-item";
                        item.style.cursor = "pointer";

                        const name = char.name.full;
                        /* most popular media title */
                        const media = char.media?.nodes?.[0]?.title?.romaji || "";

                        item.textContent = media ? `${name} (${media})` : name;

                        item.addEventListener("click", () => {
                            inputCharacter.value = name;
                            selectedCharacter = name;
                            suggestionBox.innerHTML = "";
                        });

                        suggestionBox.appendChild(item);
                    });
                }

            } catch (error) {
                console.error("Error fetching suggestions", error);
            }
        }

        // Hide suggestions when clicking outside
        document.addEventListener("click", (e) => {
            if (!suggestionBox.contains(e.target) && e.target !== inputCharacter) {
                suggestionBox.innerHTML = "";
            }
        });
    }






    // Cover Image Gamemode ------------------------------
    if (inputCover){

        inputCover.addEventListener("input", () => {
            const queryText = inputCover.value.trim();

            // Cancel previous timer to avoid spam
            clearTimeout(timeout);

            if (queryText.length < 1) {
                suggestionBox.innerHTML = "";
                return;
            }

            timeout = setTimeout(() => {
                fetchSuggestionsAnimes(queryText);
            }, 500); // delay to avoid calling on every keystroke
        });

        async function fetchSuggestionsAnimes(search) {
            const query = `
            query ($search: String, $perPage: Int) {
                Page(perPage: $perPage) {
                    media(search: $search, type: ANIME) {
                        id
                        title { 
                            romaji 
                            english
                        }
                    }
                }
            }`;

            const variables = {
                search,
                "perPage": N_RESULTS_PER_PAGE
            };

            try {
                const res = await fetch("https://graphql.anilist.co", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query, variables })
                });

                const data = await res.json();
                const media = data.data.Page.media;
                
                const filtered = media.filter(item => {
                    const romaji = item.title.romaji?.toLowerCase() || "";
                    const english = item.title.english?.toLowerCase() || "";
                    const lowerSearch = search.toLowerCase();

                    return romaji.includes(lowerSearch) || english.includes(lowerSearch);
                });
                
                const results = filtered.length > 0 ? filtered : null;
                
                if (results === null) {
                    suggestionBox.innerHTML = "<div class='text-muted px-2 py-1'>No results found</div>";
                    return;
                }
                else {
                    suggestionBox.innerHTML = "";
                    results.forEach(media => {
                        const item = document.createElement("div");
                        item.className = "p-2 suggestion-item";
                        item.style.cursor = "pointer";

                        const romaji = media.title.romaji || "";
                        const english = media.title.english || "";

                        item.innerHTML = `<strong>${romaji}</strong> ${english ? `– <em>${english}</em>` : ""}`;

                        item.addEventListener("click", () => {
                            inputCover.value = romaji;
                            selectedAnime = romaji;
                            suggestionBox.innerHTML = "";
                        });

                        suggestionBox.appendChild(item);
                    });
                }

            } catch (error) {
                console.error("Error fetching suggestions", error);
            }
        }

        // Hide suggestions when clicking outside
        document.addEventListener("click", (e) => {
            if (!suggestionBox.contains(e.target) && e.target !== inputCover) {
                suggestionBox.innerHTML = "";
            }
        });
    }
    
})