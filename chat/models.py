from django.db import models
from django.contrib.auth import get_user_model

# room 
class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_name = models.TextField(max_length=50)
    host = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='room_admin')
    room_mempers = models.ManyToManyField(get_user_model())
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name


# messages table
class Message(models.Model):
    sender = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="received_messages"
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)  # this to store the message status

    def __str__(self):
        return f"{self.sender} send to {self.receiver} in room: {self.Room.name}"
