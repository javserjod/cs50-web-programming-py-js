document.addEventListener('DOMContentLoaded', () => {

    const originalImage = document.getElementById("image-original");
    const modifiedImage = document.getElementById("image-modified");
    const imageAlternateContainer = document.getElementById("image-alternate-container");


    if (imageAlternateContainer){
        const roundState = imageAlternateContainer.dataset.roundState;
        
        if (roundState === "CORRECT") {
            imageAlternateContainer.classList.add("glow-correct");
        } else if (roundState === "WRONG") {
            imageAlternateContainer.classList.add("glow-wrong");
        }


        imageAlternateContainer.addEventListener("click", () => {
        originalImage.classList.toggle("hidden");
        modifiedImage.classList.toggle("hidden");
        });
    }
    
});