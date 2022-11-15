from .models import contacto
from rest_framework import serializers



class contacto_serial (serializers.ModelSerializer):
    class Meta:
        model = contacto
        fields = '__all__'