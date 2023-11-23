from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages


from .models import Room


@login_required(login_url="authentication:login_user")
def index(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        if room_name is not None:
            username = request.session.get("username")
            current_user = get_user_model().objects.get(username=username)

            rooms = Room.objects.filter(room_name__icontains=room_name).order_by(
                "-timestamp"
            )

            # return rooms that i memper in only
            my_rooms = []
            for room in rooms:
                if current_user in room.room_mempers.all():
                    my_rooms.append(room)

        context = {
            "page_name": "chat",
            "rooms": my_rooms,
        }
        return render(request, "chat/index.html", context)

    context = {
        "page_name": "chat",
    }
    return render(request, "chat/index.html", context)


@login_required(login_url="authentication:login_user")
def room(request, room_id):
    room = Room.objects.get(id=room_id)

    username = request.session.get("username")
    current_user = get_user_model().objects.get(username=username)

    context = {
        "page_name": room.room_name,
        "room": room,
    }

    if current_user in room.room_mempers.all():
        return render(request, "chat/room.html", context)
    else:
        messages.error(request, "You are unauthorized to access this room.")
        return render(request, 'chat/room.html', context)
