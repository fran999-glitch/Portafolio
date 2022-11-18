from app.models import *
from datetime import date
from django.utils.html import format_html



def get_categorias_choices():
	return [
	(value.pk, value.nombre) for value in Categoria.objects.all()
	]


def set_user(obj):
    return f"{obj.user.first_name} {obj.user.last_name}"
set_user.short_description = 'Usuario'

