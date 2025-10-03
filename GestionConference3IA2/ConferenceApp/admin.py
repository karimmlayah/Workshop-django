from django.contrib import admin
from .models import Conference, Submission

# Register your models here.
admin.site.site_header = "Gestion des conférences"
admin.site.site_title = "Gestion des conférences 25/26"
admin.site.index_title = "Bienvenue dans django App Conference"

admin.site.register(Conference)
admin.site.register(Submission)
