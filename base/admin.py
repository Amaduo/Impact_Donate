from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message, User, Donation, Subscriber, ContactMessage, Recent_Donation

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Donation)
admin.site.register(Recent_Donation)
admin.site.register(Subscriber)
admin.site.register(ContactMessage)