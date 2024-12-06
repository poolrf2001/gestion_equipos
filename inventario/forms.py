from django import forms
from .models import Mantenimiento, Inventario, Area

class MantenimientoForm(forms.ModelForm):
    TAREAS_CHOICES = [
        ('Inspección inicial', 'Inspección inicial'),
        ('Limpieza interna y externa', 'Limpieza interna y externa'),
        ('Revisión de conexiones internas y externas', 'Revisión de conexiones internas y externas'),
        ('Actualización de software y controladores', 'Actualización de software y controladores'),
        ('Verificación de estado del disco duro', 'Verificación de estado del disco duro'),
        ('Pruebas de funcionamiento', 'Pruebas de funcionamiento'),
        ('Activación de Windows', 'Activación de Windows'),
        ('Activación de Office', 'Activación de Office'),
        ('Otros', 'Otros'),
    ]

    # Campo dinámico para las tareas realizadas
    tareas_realizadas = forms.MultipleChoiceField(
        choices=TAREAS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tareas Realizadas"
    )
    tareas_otros = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Especificar tarea adicional...'}),
        label="Especificar Tarea (Otros)"
    )

    # Campo adicional para Área
    area = forms.ModelChoiceField(
        queryset=Area.objects.all(),
        required=True,
        label="Área",
        widget=forms.Select(attrs={"onchange": "filterInventariosByArea()"})
    )

    # Campo para mostrar el responsable del área
    responsable_area = forms.CharField(
        required=False,
        label="Responsable del Área",
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Mantenimiento
        fields = '__all__'

    class Media:
        js = ('admin/js/tareas.js', 'admin/js/inventario.js')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inicializar inventario vacío
        self.fields['inventario'].queryset = Inventario.objects.none()
        self.fields['responsable_area'].widget.attrs.update({'readonly': True})  # Campo solo lectura

        # Cargar datos si el área está seleccionada
        if 'area' in self.data:
            try:
                area_id = int(self.data.get('area'))
                self.fields['inventario'].queryset = Inventario.objects.filter(area_actual_id=area_id)

                # Configurar responsable del área
                area = Area.objects.filter(id=area_id).first()
                if area:
                    self.fields['responsable_area'].initial = area.responsable
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Si estamos editando un mantenimiento existente
            self.fields['inventario'].queryset = self.instance.area_actual.inventario_set.all()
            if self.instance.area_actual:
                self.fields['responsable_area'].initial = self.instance.area_actual.responsable



    def clean(self):
        cleaned_data = super().clean()
        tareas_realizadas = cleaned_data.get('tareas_realizadas')
        tareas_otros = cleaned_data.get('tareas_otros')

        # Validar si seleccionó "Otros" pero no especificó
        if 'Otros' in tareas_realizadas and not tareas_otros:
            self.add_error('tareas_otros', 'Debe especificar una tarea si selecciona "Otros".')
        return cleaned_data

from django import forms
from .models import Periferico, Area, Inventario

class PerifericoForm(forms.ModelForm):
    area_actual = forms.ModelChoiceField(
        queryset=Area.objects.all(),
        required=True,
        label="Área",
        widget=forms.Select(attrs={"onchange": "filterEquiposByArea()"})
    )

    class Meta:
        model = Periferico
        fields = '__all__'
    
    class Media:
        js = ('admin/js/periferico.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inicializar el campo `equipo_principal` vacío
        self.fields['equipo_principal'].queryset = Inventario.objects.none()

        # Si ya hay un área seleccionada
        if 'area_actual' in self.data:
            try:
                area_id = int(self.data.get('area_actual'))
                self.fields['equipo_principal'].queryset = Inventario.objects.filter(area_actual_id=area_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:  # Si estamos editando un periférico existente
            self.fields['equipo_principal'].queryset = Inventario.objects.filter(area_actual=self.instance.area_actual)
