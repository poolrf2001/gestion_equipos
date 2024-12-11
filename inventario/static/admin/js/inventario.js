document.addEventListener('DOMContentLoaded', function () {
    // Referencias de campos
    const detalleBienField = document.querySelector('#id_detalle_bien');
    const areaField = document.querySelector('#id_area');
    const inventarioField = document.querySelector('#id_inventario');

    const additionalFields = [
        'id_procesador',
        'id_generacion',
        'id_velocidad',
        'id_ram',
        'id_capacidad_disco',
        'id_tipo_disco',
        'id_sistema_operativo',
    ];
    const modeloFieldId = 'id_modelo'; // ID del campo modelo

    // Función para mostrar/ocultar campos según el valor de `detalle_bien`
    function toggleFields() {
        if (!detalleBienField) {
            console.error('Campo detalle_bien no encontrado.');
            return;
        }

        const value = detalleBienField.value;

        // Mostrar u ocultar los campos adicionales
        const showAdditionalFields = ['CPU', 'All in One', 'Laptop'].includes(value);
        additionalFields.forEach(fieldId => {
            const fieldElement = document.getElementById(fieldId);
            if (fieldElement) {
                const fieldWrapper = fieldElement.closest('.form-row');
                if (fieldWrapper) {
                    fieldWrapper.style.display = showAdditionalFields ? '' : 'none';
                } else {
                    console.error(`No se encontró el contenedor de ${fieldId}`);
                }
            } else {
                console.error(`Campo ${fieldId} no encontrado.`);
            }
        });

        // Mostrar u ocultar el campo modelo
        const modeloWrapper = document.getElementById(modeloFieldId)?.closest('.form-row');
        if (modeloWrapper) {
            modeloWrapper.style.display = value === 'Impresora' ? '' : 'none';
        } else {
            console.error(`Campo modelo (${modeloFieldId}) no encontrado.`);
        }
    }

    // Función para filtrar el campo "Inventario" según el área seleccionada
    function filterInventariosByArea() {
        const selectedArea = areaField?.value;
        if (!areaField || !inventarioField) {
            console.error('Campo area o inventario no encontrado.');
            return;
        }

        // Limpiar las opciones existentes
        inventarioField.innerHTML = "<option value=''>---------</option>";

        if (selectedArea) {
            fetch(`/api/inventarios_por_area/${selectedArea}/`)
                .then(response => response.json())
                .then(data => {
                    console.log('Inventarios recibidos:', data);
                    data.forEach(item => {
                        const option = document.createElement('option');
                        option.value = item.id;
                        option.textContent = `${item.codigo_inventario} (${item.detalle_bien})`;
                        inventarioField.appendChild(option);
                    });
                })
                .catch(error => console.error("Error al cargar los inventarios:", error));
        }
    }

    // Inicializar la lógica de mostrar/ocultar campos
    toggleFields();

    // Escuchar cambios en `detalle_bien`
    detalleBienField?.addEventListener('change', toggleFields);

    // Escuchar cambios en `area` para filtrar inventarios
    areaField?.addEventListener('change', filterInventariosByArea);
});
