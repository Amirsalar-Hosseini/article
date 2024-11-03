from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView

app_name = 'article'
urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('update/<int:pk>/', ArticleUpdateView.as_view(), name='article-update'),
]