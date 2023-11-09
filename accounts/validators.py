from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] # image.jpg, then 1 is jpg
    print(ext)
    valid_etensions = ['.jpg', '.png', '.jpeg'] # choose what file is valid
    if not ext.lower() in valid_etensions:
        raise ValidationError("Unsupported file. Allow files:" + str(valid_etensions))