from django.shortcuts import render
from models import Brinquedos

def index(request):
	b = Brinquedos()
	return render(request, 'inicial.html', {'b' : b})


