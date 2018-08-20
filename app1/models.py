from django.db import models
from django.contrib.auth.models import User

class requset_pu(models.Model):
    time_saved = models.DateTimeField(auto_now_add=True)
    request_kind = (
        ('1','اضطراری'),
        ('2','فوری'),
        ('3','عادی')
    )
    combo_kind = models.CharField(choices = request_kind,max_length=120)
    title = models.CharField(max_length = 60)
    dead_line = models.CharField(max_length =  500)
    ex_request = models.TextField()
    r_user = models.ForeignKey(User,on_delete = models.CASCADE)

