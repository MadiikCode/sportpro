from django import forms
from .models import SportCategory

class SportCategoryForm(forms.ModelForm):
    class Meta:
        model = SportCategory
        fields = ['name', 'description', 'image', 'rules', 'equipment', 'popular_countries']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'rules': forms.Textarea(attrs={'rows': 4}),
            'equipment': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Название вида спорта',
            'image': 'Изображение',
            'rules': 'Основные правила',
            'equipment': 'Необходимое оборудование',
            'popular_countries': 'Популярные страны'
        }