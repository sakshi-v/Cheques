from django.db import models

# Create your models here.

class Account(models.Model):
    account_number = models.CharField(max_length=50)
    account_type = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=50, decimal_places=2)
    name = models.CharField(max_length=50)
    number_of_chequebooks = models.IntegerField(max_length=50)
    def __unicode__(self):
        return self.account_number

class Cheque(models.Model):
    cheque_number = models.IntegerField(max_length=6)
    date = models.DateField()
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    payee_name = models.CharField(max_length=50)
    micr_number = models.IntegerField(max_length=9)
    account_number = models.ForeignKey(Account)
    status = models.CharField(max_length=30)
    def __unicode__(self):
        return self.cheque_number

class ChequeBook(models.Model):
    account_number = models.ForeignKey(Account)
    size = models.IntegerField(max_length=11)
    issue_date = models.DateField('issue date')
    first_cheque_number = models.IntegerField(max_length=6)
    #def __unicode__(self):
     #   return self.account_number_id

class Employee(models.Model):
    employee_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __unicode__(self):
        return self.employee_id

class Customer(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    account_number = models.ForeignKey(Account)
    def __unicode__(self):
        return self.username

class Transaction(models.Model):
    transaction_id = models.IntegerField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    from_account_number = models.ForeignKey(Account)
    to_account_number = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    employee_id = models.ForeignKey(Employee)
    def __unicode__(self):
        return self.transaction_id
    






