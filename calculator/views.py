import requests 
from django.shortcuts import render, redirect 
from django.contrib import messages

from .forms import ComputeForm
from . import services

# Create your views here.
def index(request):
    """
    GET: show the compute form populated with available operations.
    POST: Submit a compute request to FastAPI and display the result. 
    """
    try: 
        operations = services.get_operations()
    except requests.RequestException:
        operations = []
        messages.error(request, 'Could not reach the calculator service.')

    result = None 
    form = ComputeForm(operations=operations)

    if request.method == 'POST':
        form = ComputeForm(request.POST, operations=operations)
        if form.is_valid():
            data = form.cleaned_data
            try: 
                result = services.compute(
                    operation=data['operation'],
                    a=data['a'],
                    b=data['b'] or 0.0,
                )
            except requests.HTTPError as e:
                detail = e.response.json().get('detail', str(e))
                messages.error(request, f'Calculation error: {detail}')
            except requests.RequestException:
                messages.error(request, 'Could not reach the calculator service.')

    return render(request, 'calculator/index.html', {'form': form, 'result': result,})

def history(request):
    """Display or clear computation history."""
    if request.method == 'POST':        # Clear history button 
        try: 
            services.clear_history()
            messages.success(request, 'History cleared.')
        except requests.RequestException:
            messages.error(request, 'Could not reach the calculator service.')
        return redirect('calculator:history')
    
    try:
        entries = services.get_history()
    except requests.RequestException:
        entries = []
        messages.error(request, 'Could not reach the calculator service.')

    return render(request, 'calculator/history.html', {'entries': entries})

