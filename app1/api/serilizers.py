from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from app1.models import requset_pu
class requestserilizer(serializers.Serializer):
    added_var = serializers.IntegerField()
