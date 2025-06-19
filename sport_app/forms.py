from django import forms
from .models import SportCategory, Category

class SportCategoryForm(forms.ModelForm):
    class Meta:
        model = SportCategory
        category = forms.ModelChoiceField(queryset=Category.objects.all())
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
            'popular_countries': 'Популярные страны',
            category: 'Категория'
        }