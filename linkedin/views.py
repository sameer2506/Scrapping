from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


# Create your views here.

class Testing(View):
    def get(self, request):
        response = {
            "message": "Sameer Kumar"
        }

        return JsonResponse(response)
