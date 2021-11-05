from django.contrib import admin

# Register your models here.
from django.contrib import admin
from book_re.models import *

# Register your models here.
admin.site.register(Bookrating)
admin.site.register(Books)
admin.site.register(Cart)
admin.site.register(User_cast)