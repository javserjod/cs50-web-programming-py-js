document.addEventListener("DOMContentLoaded", () => {
    
    const sent_data_container = document.getElementById("round-answer-data-container");
    
    if (sent_data_container){
        

        const source = sent_data_container.dataset.gameSource;
        const correct_answer_id = sent_data_container.dataset.roundDbId;
        const gamemode = sent_data_container.dataset.gameMode;

        console.log("id:", correct_answer_id);
        
        if (gamemode === "Cover Image") {
            fetchSuggestionsMedia(correct_answer_id);

        } else if (gamemode === "Character Image") {
            fetchSuggestionsCharacter(correct_answer_id);
        }

        async function fetchSuggestionsMedia(correct_answer_id) {
            const query = `
            query ($id: Int) {
                Media(id: $id) {
                    id
                    title {
                        romaji
                        english
                    }
                    description
                    episodes
                    volumes
                    genres
                    averageScore
                    seasonYear
                    format

                }
            }`;

            const variables = {
                "id": correct_answer_id,
            };

            try {
                const res = await fetch("https://graphql.anilist.co", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query, variables })
                });

                const data = await res.json();
                const media = data.data.Media

                if (media.title.english != null && media.title.english !== media.title.romaji) {
                    document.getElementById("other-name").textContent = media.title.english;
                }
                
                const desc = media.description || "No description available.";
                const genreList = media.genres?.join(", ") || null;
                const eps = media.episodes;
                const vols = media.volumes;
                const score = media.averageScore;
                const year = media.seasonYear;
                const format = media.format;

                // <li> only if available
                const genreItem = genreList ? `<li class="list-group-item"><strong>Genres:</strong> ${genreList}</li>` : "";
                const epsItem = eps != null ? `<li class="list-group-item"><strong>Episodes:</strong> ${eps}</li>` : "";
                const volsItem = vols != null ? `<li class="list-group-item"><strong>Volumes:</strong> ${vols}</li>` : "";
                const scoreItem = score != null ? `<li class="list-group-item"><strong>Average Score:</strong> ${score}/100</li>` : "";
                const yearItem = year != null ? `<li class="list-group-item"><strong>Season Year:</strong> ${year}</li>` : "";
                const formatItem = format ? `<li class="list-group-item"><strong>Format:</strong> ${format}</li>` : "";

                // HTML
                const html = `
                    <div class="card my-4 shadow-sm" style="max-width: 700px; margin: 0 auto;">
                        <div class="card-header bg-secondary text-white">
                            <h5 class="mb-0">Additional info</h5>
                        </div>
                        <div class="card-body pb-0">
                            <p class="mb-3 text-muted" style="font-size: 0.95rem;">${desc}</p>
                            <ul class="list-group list-group-flush mb-3">
                                ${genreItem}
                                ${epsItem}
                                ${volsItem}
                                ${scoreItem}
                                ${yearItem}
                            </ul>
                        </div>
                    </div>
                `;

                const container = document.getElementById("round-details-container");
                container.innerHTML = html;

                //console.log("Fetched media data:", media);

            }catch (error) {
                console.error("Error fetching media suggestions:", error);
            }
        } 

        
        async function fetchSuggestionsCharacter(correct_answer_id) {
            const query = `
                query ($id: Int) {
                    Character(id: $id) {
                        name {
                            full
                            alternative
                        }
                        description
                        media(perPage: 30, sort: POPULARITY_DESC) {
                            edges {
                                characterRole
                                node {
                                    id
                                    title {
                                        romaji
                                        english
                                    }
                                    type
                                    format
                                    coverImage {
                                        large
                                    }
                                }
                            }
                        }
                    }
                }`;

            const variables = {
                "id": correct_answer_id,
            };

            try {
                const res = await fetch("https://graphql.anilist.co", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query, variables })
                });
                
                const data = await res.json();
                const character = data.data.Character
                const mediaEdges = character.media.edges;
                console.log("role", mediaEdges[0]);

                console.log("Character media edges:", mediaEdges);

                
                if (character.name.alternative != null && character.name.alternative !== character.name.full) {
                    if (character.name.alternative.length > 0) {
                        const firstThree = character.name.alternative.slice(0, 3);  // get to 3
                        document.getElementById("other-name").textContent = firstThree.join(", ");
                    }
                    document.getElementById("other-name").textContent = character.name.alternative.join(", ");
                }
                console.log("Character data:", character);
                
                const desc = character.description || "No description available.";

                // HTML
                const html = `
                    <div class="card my-4 shadow-sm" style="max-width: 700px; margin: 0 auto;">
                        <div class="card-header bg-secondary text-white">
                            <h5 class="mb-0">Additional info</h5>
                        </div>
                        <div class="card-body pb-0">
                            <p class="mb-3 text-muted" style="font-size: 0.95rem;">${desc}</p>
                            
                        </div>
                    </div>
                `;

                const infoContainer = document.getElementById("round-details-container");
                infoContainer.innerHTML = html;

                const characterParticipationsContainer = document.getElementById("character-participations");

                mediaEdges.forEach(edge => {
                    const titleRomaji = edge.node.title.romaji;
                    const titleEnglish = edge.node.title.english;
                    const role = edge.characterRole;
                    const format = edge.node.format;
                    const cover = edge.node.coverImage.large;

                    const mediaItem = document.createElement("div");
                    mediaItem.className = "card mb-3 p-2 d-flex flex-column";
                    mediaItem.style.width = "200px";
                    mediaItem.innerHTML = `
                        <img src="${cover}" alt="${titleRomaji}" class="card-img-top mx-auto d-block" style="width: 100%; height: 250px; object-fit: fill;"> 
                        <div class="card-body d-flex flex-column justify-content-between p-2" style="flex: 1;">
                            <h6 class="card-title mb-1">${titleRomaji} ${titleEnglish ? `(<em>${titleEnglish}</em>)` : ""}</h6>
                            <small class="text-muted">${role} in ${format}</small>
                        </div>
                    `;
                    characterParticipationsContainer.appendChild(mediaItem);
                    
                })

                //console.log("Fetched media data:", media);

            }catch (error) {
                console.error("Error fetching media suggestions:", error);
            }
        } 


    }

});