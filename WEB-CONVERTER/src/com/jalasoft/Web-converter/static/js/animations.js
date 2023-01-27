window.onload = function() {
    // Select the button and images
    const button = document.getElementById("show-example-button");
    const image1 = document.getElementById("image-1");
    const image2 = document.getElementById("image-2");

    // Add an event listener to the button
    button.addEventListener("click", function() {
        // Add the "active" class to the first image and remove it from the second image
        image1.classList.add("active");
        image2.classList.remove("active");

        // Listen for the animation end event on the first image
        image1.addEventListener("animationend", function() {
            // Show the "watch again" button
            document.getElementById("watch-again-button").style.display = "block";
        });
    });

    // Add an event listener to the "watch again" button
    const watchAgainButton = document.getElementById("watch-again-button");
    watchAgainButton.addEventListener("click", function() {
        // Hide the "watch again" button
        this.style.display = "none";

        // Add the "active" class to the second image and remove it from the first image
    image2.classList.add("active");
    image1.classList.remove("active");
});
