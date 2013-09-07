# Create your views here.
from django.shortcuts import render ,render_to_response
def mobile(request):
    return render(request, 'mobile.html', {'current_date': 'now'})
