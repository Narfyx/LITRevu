document.addEventListener("DOMContentLoaded", function () {
  // Fonction pour créer et insérer le compteur de caractères
  function createCharCounter(element) {
    const maxLength = element.getAttribute("maxlength");

    // Créez dynamiquement un élément pour afficher le compteur de caractères
    const charCountDiv = document.createElement("div");
    charCountDiv.className = "charCount";
    charCountDiv.textContent = ` 0 / ${maxLength}`;

    // Insérez le div après l'élément
    element.parentNode.insertBefore(charCountDiv, element.nextSibling);

    // Ajoutez un écouteur d'événements pour mettre à jour le compteur de caractères
    element.addEventListener("input", function () {
      const currentLength = element.value.length;
      charCountDiv.textContent = `${currentLength} / ${maxLength}`;
    });
  }

  // Sélectionnez tous les éléments <textarea> et <input> de type texte avec un attribut maxlength
  const elements = document.querySelectorAll(
    'textarea[maxlength], input[type="text"][maxlength]'
  );

  // Appliquez la fonction de compteur de caractères à chacun de ces éléments
  elements.forEach(function (element) {
    createCharCounter(element);
  });
});
