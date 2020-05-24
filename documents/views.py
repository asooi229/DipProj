from django.http.response import JsonResponse
from django.views.generic.base import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.contrib.auth import authenticate
from django.utils import timezone

import DIPLOM.text_recognition

class OcrFormView(TemplateView):
    template_name = 'documents/ocr_form.html'
ocr_form_view = OcrFormView.as_view()


class OcrView(View):
    def post(self, request, format=None):
    
        file_obj = request.FILES.get('image', None)
        if file_obj:
            utf8_text = ocr_with_django.text_recognition.transcript(file_obj)
            return JsonResponse({'utf8_text': utf8_text}, status=200)
        return JsonResponse({}, status=204)

ocr_view = csrf_exempt(OcrView.as_view())

def mainpg(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_users=User.objects.all().count()
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Отрисовка HTML-шаблона index.html с данными внутри 
    # переменной контекста context
    return render(
        request,
        'mainpg.html',
        context={'num_users':num_users,'num_visits':num_visits},
    )
def about_us(request):
     return render(
        request,
        'about_us.html',
        
    )
