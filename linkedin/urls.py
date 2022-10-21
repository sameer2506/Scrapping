from django.urls import path

from linkedin.views import Testing, ListOfAllProfiles

urlpatterns = [
    path('testing', Testing.as_view()),
    path('listOfAllProfiles', ListOfAllProfiles.as_view())
]
