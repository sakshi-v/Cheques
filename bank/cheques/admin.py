from cheques.models import Account, Cheque, ChequeBook
from django.contrib import admin

class AccountAdmin(admin.ModelAdmin):
    search_fields = ['account_number']

admin.site.register(Account,AccountAdmin)
admin.site.register(Cheque)
admin.site.register(ChequeBook)
