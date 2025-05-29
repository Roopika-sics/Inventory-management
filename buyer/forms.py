from django import forms
from products.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'image']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'How was the product', 'rows': 4, 'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 5, 'class': 'form-range'}),
        }