from django.urls import path

from search.views import ListProjects

urlpatterns = [
    path('', ListProjects.as_view())
]
