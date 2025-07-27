from django.contrib import admin
from django.urls import path

from menu.views import MenuView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MenuView.as_view(), name='tree'),
    path('<path:path>/', MenuView.as_view(), name='tree_active'),
]
