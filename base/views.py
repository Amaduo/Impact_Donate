from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, MyUserCreationForm
from .models import Donation
from .forms import DonationForm
from .forms import ContactForm
from .forms import SubscriptionForm
from .forms import UserForm
from . mpesa import AccessToken, Password
import requests





def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscription successful!")
            return redirect("subscribe")  # Change this to your desired redirect URL
    else:
        form = SubscriptionForm()
    return render(request, "subscribe.html", {"form": form})


def contact_view(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')  # Redirect to the same page after submission

    return render(request, 'contact.html', {'form': form})

def donation_view(request):
    if request.method == "POST":
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('donation_success')
    else:
        form = DonationForm()
    donations = Donation.objects.all()
    return render(request, 'donations.html', {'form': form, 'donations': donations})

def donation_success(request):
    return render(request, 'donation_success.html')

def recent_donations(request):
    donations = Donation.objects.all().order_by('-id')  if Donation.objects.exists() else []  # Fetch recent donations
    return render(request, 'recent_donations.html', {'donations': donations})

def donation_list(request):
    donations = Donation.objects.all()  # Fetch donations
    return render(request, 'recent_donations.html', {'donations': donations})

def donation_page(request):
    if request.method == "POST":
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('thank_you')  # Redirect to Thank You page
    else:
        form = DonationForm()

    donations = Donation.objects.order_by('-created_at')[:6]  # Show last 6 donations
    return render(request, 'donations.html', {'form': form, 'donations': donations})

def recent_donations(request):
    donations = Donation.objects.order_by('-created_at')  # Show all donations
    return render(request, 'recent_donations.html', {'donations': donations})

def thank_you(request):
    return render(request, 'thank_you.html')

def donation_page(request):
    if request.method == "POST":
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recent_donations')  # Redirect to Recent Donations after submission
    else:
        form = DonationForm()

    return render(request, 'donation_page.html', {'form': form})

def recent_donations(request):
    donations = Donation.objects.order_by('-id')  # Show latest donations first
    return render(request, 'recent_donations.html', {'donations': donations})


def edit_donation(request, donation_id):  
    donation = get_object_or_404(Donation, id=donation_id)
    if request.method == "POST":
        form = DonationForm(request.POST, request.FILES, instance=donation)  
        if form.is_valid():
            form.save()
            return redirect('donation_page')  
    else:
        form = DonationForm(instance=donation)
    return render(request, 'donations/edit_donation.html', {'form': form, 'donation': donation})  



def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            # Display specific error messages from the form
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    return render(request, 'base/login_register.html', {'form': form})



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.rooms.all()  # Use 'rooms' instead of 'room_set'
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = get_object_or_404(Room, id=pk)

    if request.user != room.host:
        return HttpResponseForbidden("You are not allowed to delete this room!")

    if request.method == 'POST':
        room.delete()
        messages.success(request, "Room deleted successfully!")
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})



def indexx_view(request):
    return render(request, 'indexx.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contacts.html')

def pay(request):
    return render(request, 'pay.html')



def stk(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        access_token = AccessToken.access_token
        api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        header = {"Authorization": "Bearer %s" % access_token}

        request = {    
            "BusinessShortCode": Password.short_code,    
            "Password": Password.encoded_password,    
            "Timestamp": Password.timestamp,    
            "TransactionType": "CustomerPayBillOnline",    
            "Amount": amount,    
            "PartyA": phone,    
            "PartyB": Password.short_code,    
            "PhoneNumber":phone,    
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa",    
            "AccountReference":"Charity Donation",    
            "TransactionDesc":"ImpactDonate"
            }
        

    response = requests.post(api_url, json=request, headers=header)
    return HttpResponse('PAYMENT SUCCESS, PLEASE CHECK YOUR PHONE TO COMPLETE TRANSACTION!!')


# def stk(request):
#     if request.method == 'POST':
#         phone = request.POST.get('phone')
#         amount = request.POST.get('amount')

#         if not phone or not amount:
#             return HttpResponse("Phone number and amount are required.", status=400)

#         access_token = AccessToken.access_token
#         api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
#         headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

#         payload = {    
#             "BusinessShortCode": Password.short_code,    
#             "Password": Password.encoded_password,    
#             "Timestamp": Password.timestamp,    
#             "TransactionType": "CustomerPayBillOnline",    
#             "Amount": int(amount),  # Ensure the amount is an integer    
#             "PartyA": phone,    
#             "PartyB": Password.short_code,    
#             "PhoneNumber": phone,    
#             "CallBackURL": "https://yourdomain.com/mpesa_callback",  # Change to your actual callback URL    
#             "AccountReference": "Charity Donation",    
#             "TransactionDesc": "ImpactDonate"
#         }

#         response = requests.post(api_url, json=payload, headers=headers)

#         try:
#             response_data = response.json()
#         except ValueError:
#             return HttpResponse("Invalid response from Safaricom API.", status=500)

#         if response_data.get("ResponseCode") == "0":
#             return HttpResponse("PAYMENT SUCCESS, PLEASE CHECK YOUR PHONE TO COMPLETE TRANSACTION!")
#         else:
#             return HttpResponse(f"Error: {response_data.get('errorMessage', 'Transaction Failed')}", status=400)

#     return HttpResponse("Invalid request method.", status=405)