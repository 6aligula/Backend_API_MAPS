from django import forms
from leaflet.forms.widgets import LeafletWidget
from .models import Plot

class PlotForm(forms.ModelForm):
    class Meta:
        model = Plot
        fields = '__all__'
        widgets = {
            'bounds': LeafletWidget(),  # Usa el widget de Leaflet para el campo 'bounds'
        }
