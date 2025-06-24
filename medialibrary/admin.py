from django.contrib import admin
from .models import Member, Book, CD, DVD, BoardGame, Loan

admin.site.register(Member)
admin.site.register(Book)
admin.site.register(CD)
admin.site.register(DVD)
admin.site.register(BoardGame)
admin.site.register(Loan)
