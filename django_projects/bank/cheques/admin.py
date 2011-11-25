from cheques.models import Account, Cheque, ChequeBook, Employee, Customer, Transaction
from django.contrib import admin

class AccountAdmin(admin.ModelAdmin):
    search_fields = ['account_number']

admin.site.register(Account,AccountAdmin)
admin.site.register(Cheque)
admin.site.register(ChequeBook)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Transaction)
