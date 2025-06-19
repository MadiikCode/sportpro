from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Q
from .models import SportCategory, Category
from .forms import SportCategoryForm

from django.views.generic import DetailView
from .models import SportCategory


class SportListView(ListView):
    """Класс-представление для списка видов спорта с пагинацией и поиском"""
    model = SportCategory
    template_name = 'sport_app/sport_list.html'
    context_object_name = 'sports'  # Изменили на 'sports' для соответствия шаблону
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        category_id = self.request.GET.get('category')  # Получаем ID категории из запроса

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if category_id:  # Фильтруем по категории, если она выбрана
            queryset = queryset.filter(category_id=category_id)

        return queryset.order_by('-created_at')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['categories'] = Category.objects.all()  # Все категории для фильтрации
        context['selected_category'] = self.request.GET.get('category', '')  # Выбранная категория
        return context

@login_required

def add_sport(request):
    if request.method == 'POST':
        form = SportCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            sport = form.save(commit=False)
            sport.author = request.user
            sport.save()
            messages.success(request, f'Вид спорта "{sport.name}" успешно добавлен!')
            return redirect('sport_app:sport_list')  # Редирект на главную
    else:
        form = SportCategoryForm()
    return render(request, 'sport_app/add_sport.html', {'form': form})


@login_required
def edit_sport(request, sport_id):
    """Редактирование вида спорта с проверкой прав доступа"""
    sport = get_object_or_404(SportCategory, id=sport_id)

    # Проверка прав доступа
    if not request.user.is_superuser and request.user != sport.author:
        messages.error(request, 'У вас нет прав для редактирования этой записи!')
        return redirect('sport_app:sport_list')

    if request.method == 'POST':
        form = SportCategoryForm(request.POST, request.FILES, instance=sport)
        if form.is_valid():
            # Сохраняем только если изображение было изменено
            if 'image-clear' in request.POST:
                sport.image.delete(save=False)

            updated_sport = form.save()
            messages.success(request, f'Изменения для "{updated_sport.name}" сохранены!')
            return redirect('sport_app:sport_list')
    else:
        form = SportCategoryForm(instance=sport)

    return render(request, 'sport_app/edit_sport.html', {
        'form': form,
        'sport': sport,
        'title': f'Редактирование: {sport.name}'
    })


@login_required
def delete_sport(request, sport_id):
    """Удаление вида спорта с подтверждением"""
    sport = get_object_or_404(SportCategory, id=sport_id)

    if not request.user.is_superuser and request.user != sport.author:
        messages.error(request, 'У вас нет прав для удаления этой записи!')
        return redirect('sport_app:sport_list')

    if request.method == 'POST':
        sport_name = sport.name
        sport.delete()
        messages.success(request, f'Вид спорта "{sport_name}" успешно удален!')
        return redirect('sport_app:sport_list')

    return render(request, 'sport_app/delete_sport.html', {
        'sport': sport,
        'title': f'Удаление: {sport.name}'
    })

class SportDetailView(DetailView):
    model = SportCategory
    template_name = 'sport_app/sport_detail.html'
    context_object_name = 'sport'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем средний рейтинг для отображения звезд
        context['sport'].user_rating = self.object.average_rating()
        return context