from __future__ import unicode_literals

from django.db import models
from ..login_reg.models import User
from datetime import datetime, date

# Create your models here.
class FriendManager(models.Manager):
    def create(self, id):
        friend = User.objects.get(id=id)
        print (friend.id, friend.name)
        this_friend = Friend.objects.create(friend=friend)
        print (this_friend.id, this_friend.friend.id, this_friend.friend.name)
        return (True, this_friend.id)

    def bridge_connections(self, postData):
        if not postData:
            return (False)
        else:
            user = User.objects.get(id=int(postData['user']))
            # print ('USER:', user.id, user.name, user.alias)
            friend = Friend.objects.get(id=int(postData['friend']))
            # print ('FRIEND:', friend.id, friend.name, friend.alias)

            Friendship.objects.create(user=user, friend=friend)
            return (True)


    def delete(self, postData):
        friendship = Friendship.objects.get(id=int(postData['friendship']))
        friendship.delete()
        return True


class Friend(models.Model):
    friend = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_table_id', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friendManager = FriendManager()
    objects = models.Manager()

class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
