from rest_framework import serializers
from django.contrib.auth.models import User
from myapp.models import Todo

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ["id","username","email","password"]

        read_only_fields=["id"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields="__all__"
        read_only_fields=["id","created_at","due_date","owner"]