from database.models import Author, Paper, Topic, Partner, Update, Comment

from django.contrib import admin

admin.site.register(Paper)
admin.site.register(Author)
admin.site.register(Topic)
admin.site.register(Partner)
admin.site.register(Update)
admin.site.register(Comment)