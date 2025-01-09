from django import forms
from .models import ShapefileUpload

class ShapefileUploadForm(forms.ModelForm):
    class Meta:
        model = ShapefileUpload
        fields = ['name', 'shapefile']
