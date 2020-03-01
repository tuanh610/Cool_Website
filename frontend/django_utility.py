from django.core.exceptions import ValidationError

def validate_image_file(value):
    valid_extension = ['jpg', 'png']
    for ext in valid_extension:
        if value.name.endswith(ext):
            return
    raise ValidationError('File is not of jpeg or png format')