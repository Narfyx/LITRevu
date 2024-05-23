document.addEventListener("DOMContentLoaded", function () {
  var ratings = document.querySelectorAll(".post-rating");

  ratings.forEach(function (ratingElem) {
    // Convertir la chaîne de caractères de l'attribut 'data-rating' en un entier en base 10
    var rating = parseInt(ratingElem.getAttribute("data-rating"), 10);
    if (isNaN(rating) || rating < 0 || rating > 5) {
      console.error("Invalid rating value:", ratingElem.getAttribute("data-rating"));
      return;
    }

    // Clear any previous star rating elements to avoid duplication
    ratingElem.innerHTML = "";
    // Crée un nouvel élément 'div' pour contenir les étoiles
    var starRating = document.createElement("div");
    starRating.classList.add("star-rating");

    // Définit le contenu HTML de 'starRating' pour afficher les étoiles
    // La largeur du 'span' est déterminée par la note (rating) multipliée par 20% car 5 étoiles = 100%
    starRating.innerHTML = `<span style="width: ${rating * 20}%;">★★★★★</span>`;

    // Ajoute le nouvel élément 'div' comme enfant de l'élément actuel 'ratingElem'
    ratingElem.appendChild(starRating);
  });
});
