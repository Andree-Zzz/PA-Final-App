// Obtener referencia al input y a la imagen
const $imagenInput = document.querySelector("#imagen"),
  $previewImg = document.querySelector("#previewImg");

// Escuchar cuando cambie
$imagenInput.addEventListener("change", () => {
  // Los archivos seleccionados, pueden ser muchos o uno
  const archivos = $imagenInput.files;
  // Si no hay archivos salimos de la función y quitamos la imagen
  if (!archivos || !archivos.length) {
    $previewImg.src = "";
    return;
  }
  // Ahora tomamos el primer archivo, el cual vamos a previsualizar
  const primerArchivo = archivos[0];
  // Lo convertimos a un objeto de tipo objectURL
  const objectURL = URL.createObjectURL(primerArchivo);
  // Y a la fuente de la imagen le ponemos el objectURL
  $previewImg.src = objectURL;
  $previewImg.classList = 'rounded'
});