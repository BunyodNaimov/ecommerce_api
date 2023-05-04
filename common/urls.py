from django.urls import path

from common.views import CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('', CategoryListCreateView.as_view(), name='categories_list_create'),
    path('<int:pk>', CategoryDetailView.as_view(), name='categories_detail'),
]