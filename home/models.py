from django.db import models
from accounts.models import CustUser
# Create your models here.

class Notes(models.Model):
    user=models.ForeignKey(CustUser,on_delete=models.CASCADE,related_name='notes_user',default=21)
    title=models.CharField(max_length=100,null=True)
    desc=models.TextField(null=True)
    dt=models.DateTimeField(auto_now_add=True,null=True)



class Messages(models.Model):
    user=models.ForeignKey(CustUser,on_delete=models.CASCADE,related_name='msg')
    msg=models.TextField()
    send_at=models.DateTimeField(auto_now_add=True,null=True)


class ViewedMessages(models.Model):
    msg=models.ForeignKey(Messages,on_delete=models.CASCADE,related_name='msg_view')
    user=models.ForeignKey(CustUser,on_delete=models.CASCADE,related_name='user_msg')
    viewed=models.BooleanField(default=False)
    read=models.BooleanField(default=False)
    viewed_date=models.DateTimeField(null=True)
    read_date=models.DateTimeField(null=True)
    