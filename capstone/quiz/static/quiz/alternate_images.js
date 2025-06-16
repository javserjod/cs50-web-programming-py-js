document.addEventListener('DOMContentLoaded', () => {

    const originalImage = document.getElementById("image-original");
    const modifiedImage = document.getElementById("image-modified");
    const imageAlternateContainer = document.getElementById("image-alternate-container");

    if (imageAlternateContainer){
        imageAlternateContainer.addEventListener("click", () => {
        originalImage.classList.toggle("hidden");
        modifiedImage.classList.toggle("hidden");
        });
    }
    
});