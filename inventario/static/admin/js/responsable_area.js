document.addEventListener('DOMContentLoaded', function () {
    const areaField = document.querySelector('#id_area');
    const responsableField = document.querySelector('#id_responsable_area');

    areaField.addEventListener('change', function () {
        const areaId = areaField.value;

        fetch(`/api/responsable_area/${areaId}/`)
            .then(response => response.json())
            .then(data => {
                responsableField.value = data.responsable || '';
            })
            .catch(error => console.error('Error al cargar el responsable:', error));
    });
});
