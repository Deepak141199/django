import imp
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name","phone","address"]
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"required": True},
            "phone": {"required": True},
            "email": {"required": True},
        }
        
        
        def create(self, validated_data):
            user = User.objects.create(**validated_data)
            return user
