document.addEventListener('DOMContentLoaded', function () {
    const areaField = document.querySelector('#id_area_actual');  // Campo "Área"
    const equipoPrincipalField = document.querySelector('#id_equipo_principal');  // Campo "Equipo Principal"

    // Función para filtrar equipos principales por área seleccionada
    function filterEquiposByArea() {
        const selectedArea = areaField.value;

        // Limpiar las opciones existentes en el campo "Equipo Principal"
        equipoPrincipalField.innerHTML = "<option value=''>---------</option>";

        if (selectedArea) {
            fetch(`/api/equipos_principales_por_area/${selectedArea}/`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(item => {
                        const option = document.createElement('option');
                        option.value = item.id;
                        option.textContent = `${item.codigo_inventario} (${item.detalle_bien})`;
                        equipoPrincipalField.appendChild(option);
                    });
                })
                .catch(error => console.error('Error al cargar los equipos principales:', error));
        }
    }

    // Escuchar cambios en el campo "Área"
    areaField.addEventListener('change', filterEquiposByArea);
});
