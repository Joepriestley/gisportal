import os
import zipfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from django.contrib.gis.gdal import DataSource
from django.db import models
from django.db import connection
from .models import ShapefileUpload


@receiver(post_save, sender=ShapefileUpload)
def handle_uploaded_shapefile(sender, instance, **kwargs):
    if not instance.shapefile:
        return  # Exit if no shapefile is uploaded

    file_path = instance.shapefile.path

    # Unzip if it's a zip file
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            extract_path = os.path.splitext(file_path)[0]
            zip_ref.extractall(extract_path)
        file_path = [
            os.path.join(extract_path, f) for f in os.listdir(extract_path) if f.endswith('.shp')
        ][0]

    # Load the shapefile
    try:
        data_source = DataSource(file_path)
    except Exception as e:
        print(f"Error loading shapefile: {e}")
        return

    if len(data_source) == 0:
        print("No layers found in shapefile.")
        return

    layer = data_source[0]

    # Get the target model
    try:
        model = apps.get_model('gisportal', instance.model_name)
    except LookupError:
        print(f"Model {instance.model_name} not found.")
        return

    # Process shapefile features
    for feature in layer:
        geometry = feature.geometry.geos

        # Ensure fields are converted into a dictionary correctly
        attributes = {str(field_name): feature.get(field_name) for field_name in layer.fields}

        # Validate and filter attributes for valid model fields
        valid_attributes = {
            field_name: field_value
            for field_name, field_value in attributes.items()
            if hasattr(model, field_name)
        }

        # Create or update records
        obj, created = model.objects.get_or_create(geometry=geometry, defaults=valid_attributes)

        # Dynamically add new fields if necessary
        for field_name, field_value in attributes.items():
            if not hasattr(model, field_name):
                # Add the new field dynamically
                with connection.schema_editor() as schema_editor:
                    new_field = models.CharField(max_length=255, null=True, blank=True)
                    new_field.set_attributes_from_name(field_name)
                    schema_editor.add_field(model, new_field)
                setattr(obj, field_name, field_value)

        # Save the updated object
        obj.save()

    print("Shapefile processed successfully.")
