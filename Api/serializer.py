from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Register
from .models import Poll,Option,Vote
        

class Register_serializer(serializers.ModelSerializer):
    class Meta:
        model=Register
        fields=['username','Role','email','password','id']
        
    def create(self, validated_data):
        validated_data['password']=make_password(validated_data['password'])
        return super().create(validated_data)


class Poll_serializer(serializers.ModelSerializer):
    class Meta:
        model=Poll
        fields='__all__'
        extra_kwargs={
           'created_by':{'read_only':True}
        }

        def validate_question(self,value):
            if len(value)<10:
                raise serializers.ValidationError('Question must contain at least 10 characters')

class Option_serializer(serializers.ModelSerializer):
    class Meta:
        model=Option
        fields='__all__'

class Vote_serializer(serializers.ModelSerializer):
    class Meta:
        model=Vote
        fields='__all__'
        extra_kwargs={
            'user':{'read_only':True}
        }

        def validate(self,data):
            poll=data['poll']
            option=data['option']

            if option.poll != poll:
                raise serializers.ValidationError('Selected option does not belong to this post')
