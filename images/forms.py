from urllib import request

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("title", "url", "description")

    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg"]
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("The given URL does not match valid JPEG image")
        return url

    def save(self, commit=True):
        image = super().save(commit=False)

        url = self.cleaned_data["url"]
        slug = slugify(image.title)
        extension = url.rsplit(".", 1)[1].lower()
        image_name = f"{slug}.{extension}"

        # download image from the given URL
        response = request.urlopen(url)
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit:
            image.save()
        return image
