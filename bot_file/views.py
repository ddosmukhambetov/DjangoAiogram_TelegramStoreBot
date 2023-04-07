from django.shortcuts import render


def index(request):
    return render(request, 'bot_file/index.html')
