from django.contrib import admin

from .models import Associate
from .models import Addresses
from .models import Settings
from .models import UploadFiles

admin.site.register(Associate)
admin.site.register(Addresses)
admin.site.register(Settings)
admin.site.register(UploadFiles)

