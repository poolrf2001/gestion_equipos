document.addEventListener('DOMContentLoaded', function () {
    const checkboxOtros = document.querySelector('input[value="Otros"]'); // Selecciona el checkbox de "Otros"
    const inputTareasOtros = document.querySelector('input[name="tareas_otros"]'); // Selecciona el campo de texto

    // Asegúrate de que el campo de texto esté deshabilitado al cargar la página
    if (inputTareasOtros) {
        inputTareasOtros.disabled = !checkboxOtros.checked;
    }

    // Escucha los cambios en el checkbox de "Otros"
    if (checkboxOtros) {
        checkboxOtros.addEventListener('change', function () {
            inputTareasOtros.disabled = !this.checked;
            if (!this.checked) {
                inputTareasOtros.value = ""; // Limpia el campo de texto si se desactiva
            }
        });
    }
});
