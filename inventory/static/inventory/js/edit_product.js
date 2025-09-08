document.addEventListener("DOMContentLoaded", () => {
    const inputFile = document.getElementById("id_images");
    const label = inputFile.nextElementSibling; // a span.file-label
 
    inputFile.addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (file) {
            label.textContent = file.name; // mostra o nome do arquivo
        } else {
            label.textContent = "Escolher arquivo"; // texto padrão
        }
    });
});
