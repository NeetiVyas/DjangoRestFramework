from .models import Customer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=Customer.objects.all(),
            fields=['name', 'age']
        )] 