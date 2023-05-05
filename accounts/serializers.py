
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User

#User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RefreshToken:
    pass



class LoginSerializer(serializers.Serializer):
 id = serializers.CharField(write_only=True, required=True)
 password = serializers.CharField(write_only=True, required=True)

 def validate(self, request):
     id = request.get('id', None)
     password = request.get('password', None)

     if User.objects.filter(id=id).exists():
         user = User.objects.get(id=id)
         if not user.check_password(password):
             raise serializers.ValidationError({"Wrong Password"})
     else:
         raise serializers.ValidationError({"User doesn't exist."})

     token = RefreshToken.for_user(user)
     refresh = str(token)
     access = str(token.access_token)

     data = {
         'id': user.id,
         'refresh': refresh,
         'access': access
     }

     return data
