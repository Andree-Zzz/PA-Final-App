
document.querySelector("#copy").addEventListener("click", copyToClipBoard);

function copyToClipBoard() {
    // Obtenere el texto del textarea del html
    const ContentTextArea = document.getElementById("textImage").value
    // Copiar al Portapapeles
    navigator.clipboard.writeText(ContentTextArea)
    // alert("Copiado!");
    let alert = document.getElementById("alert")
    alert.classList.remove("visually-hidden")
}
