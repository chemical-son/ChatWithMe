from django.shortcuts import render


def main(request):
    context = {
        "page_name": "Chat With Me",
    }
    return render(request, "main.html", context)