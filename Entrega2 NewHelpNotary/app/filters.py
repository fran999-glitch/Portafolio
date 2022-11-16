from dataclasses import fields
from pyexpat import model
import django_filters
from .models import*
from django_filters import DateFilter

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = [
			'username',
			'first_name',
			'last_name',
			'email',
            'is_superuser',
				 ]
