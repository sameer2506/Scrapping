from django.urls import path

from linkedin.views import Testing

urlpatterns = [
    path('testing', Testing.as_view())
]
