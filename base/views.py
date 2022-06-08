from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q

from .models import Message, Room, Topic, User
from .forms import MessageForm, RoomForm, UserForm, MyUserCreationForm


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.add_message(request, messages.ERROR, "No user found")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.add_message(request, messages.ERROR, "Incorrect credentials")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.add_message(
                request,
                messages.ERROR,
                form.errors,
            )

    context = {"form": form}
    return render(request, "base/login_register.html", context)


def home(request):
    query = request.GET.get("q") if request.GET.get("q") != None else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=query)
        | Q(name__icontains=query)
        | Q(description__icontains=query)
    )

    room_count = rooms.count()

    topics = Topic.objects.all()[0:5]

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=query))

    print(room_messages.count())

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
    }

    return render(request, "base/home.html", context)


def room(request, roomId):
    room = Room.objects.get(id=roomId)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", roomId=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def userProfile(request, userId):
    user = User.objects.get(id=userId)
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="/login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        form = RoomForm(request.POST)
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("home")

    return render(request, "base/room_form.html", {"form": form, "topics": topics})


@login_required(login_url="/login")
def updateRoom(request, roomId):
    room = Room.objects.get(id=roomId)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        HttpResponse("You are not allowed here!!!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("home")

    return render(
        request, "base/room_form.html", {"form": form, "topics": topics, "room": room}
    )


@login_required(login_url="/login")
def deleteRoom(request, roomId):
    room = Room.objects.get(id=roomId)

    if request.user != room.host:
        HttpResponse("You are not allowed here!!!")

    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "base/delete.html", {"obj": room})


@login_required(login_url="/login")
def updateMessage(request, roomId, messageId):
    message = Message.objects.get(id=messageId)
    form = MessageForm(instance=message)

    print(request.user != message.user)
    if request.user != message.user:
        return HttpResponse("You are not allowed here!!!")

    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect("room", roomId=roomId)

    return render(request, "base/message_form.html", {"form": form})


@login_required(login_url="/login")
def deleteMessage(request, roomId, messageId):
    message = Message.objects.get(id=messageId)

    if request.user != message.user:
        return HttpResponse("You are not allowed here!!!")

    if request.method == "POST":
        message.delete()
        return redirect("room", roomId=roomId)

    return render(request, "base/delete.html", {"obj": message})


@login_required(login_url="/login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", userId=user.id)

    context = {"form": form}
    return render(request, "base/update_user.html", context)


def topics(request):
    query = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=query)
    context = {"topics": topics}
    return render(request, "base/topics.html", context)


def activities(request):
    room_messages = Message.objects.all()
    context = {"room_messages": room_messages}
    return render(request, "base/activity.html", context)
