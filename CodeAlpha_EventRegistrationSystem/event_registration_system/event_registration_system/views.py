from django.shortcuts import render

def homepage(request):
    '''display homepage'''
    return render(request, 'homepage.html')