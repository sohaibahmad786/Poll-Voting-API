from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Register
from .models import Poll
from .models import Option
from .models import Vote

admin.site.register(Vote)
admin.site.register(Option)
admin.site.register(Poll)
admin.site.register(Register,UserAdmin)

# Register your models here.
