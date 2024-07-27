from django.contrib import admin
from .models import Tracker, Policy

admin.site.register([Tracker, Policy])
