from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Friend, Friendship

# Create your views here.
def index(request):
    # Friendship.objects.all().delete()
    # this = Friend.objects.filter(id=10)
    # this.delete()
    id = request.session['thisUser']
    # print(id)
    context = {
    'users':User.objects.all(),
    'thisUser':User.objects.get(id=id),
    'friends':Friend.objects.all(),
    'friendships':Friendship.objects.all(),
    }
    if ('newUser' in request.session) == True:
        # print ('new registration')
        verify = Friend.friendManager.create(id)
        if verify[0] == True:
            # print ('added to friend table')
            del request.session['newUser']
            request.session.modified = True
            return render(request, 'friends/index.html', context)
    else:
        # print ('already registered')
        return render(request, 'friends/index.html', context)

def add(request):
    if request.method == "POST":
        verify = Friend.friendManager.bridge_connections(request.POST)

        if verify == True:
            # print ('friendship created')
            return redirect(reverse('friends:index'))
        else:
            print ('something went wrong')
            return redirect(reverse('friends:index'))

def show(request, id):
    if request.method == "GET":
        context = {
            'user':User.objects.get(id=id)
        }
        return render(request, 'friends/show.html', context)

def remove(request):
    if request.method == "POST":
        destroy = Friend.friendManager.delete(request.POST)
        if destroy == True:
            return redirect(reverse('friends:index'))
