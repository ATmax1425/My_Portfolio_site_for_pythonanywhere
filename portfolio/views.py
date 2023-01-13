from django.shortcuts import render
from .forms import MessageForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def contact(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "thank_you.html")
    else:
        form = MessageForm()
        return render(request, "contact.html", {'form': form})
