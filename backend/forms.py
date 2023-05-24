from django import forms


class ImageUploadForm(forms.Form):
    image_file = forms.FileField(
        label='Image File',
        widget=forms.FileInput(
            attrs={
                'accept': 'image/jpeg,image/gif,image/png,image/webp'
            }
        )
    )
