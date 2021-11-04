from django.contrib import admin

# Register your models here.
from .models import User, Comments, Followers

admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Followers)