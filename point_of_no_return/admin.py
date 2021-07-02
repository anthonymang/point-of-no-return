from django.contrib import admin
from .models import Music, Artist, Submission, Comment, Curator

# Register your models here.
admin.site.register(Music)
admin.site.register(Artist)
admin.site.register(Submission)
admin.site.register(Comment)
admin.site.register(Curator)