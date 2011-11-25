from django.db import models



##This is used to create Account table in the database to store account information
class Account(models.Model):
	##Account number of type 'char'. This is the key of the table
    account_number = models.CharField(max_length=50)
	##Account type of type 'char'
    account_type = models.CharField(max_length=50)
	##Balance of type 'decimal'
    balance = models.DecimalField(max_digits=50, decimal_places=2)
	##Name of the account holder, type: char
    name = models.CharField(max_length=50)
	##Number of cheque books of type 'int'
    number_of_chequebooks = models.IntegerField(max_length=50)
    def __unicode__(self):
        return self.account_number

##This is used to create Cheque table in the database to store cheque information
class Cheque(models.Model):
	##cheque number present on the cheque type: int
    cheque_number = models.IntegerField(max_length=6)
	##cheque issue date type: date
    date = models.DateField()
	##Cheque amount type: decimal
    amount = models.DecimalField(max_digits=50, decimal_places=2)
	##Payee name ype: char
    payee_name = models.CharField(max_length=50)
	##micr number present on cheque, type: int
    micr_number = models.IntegerField(max_length=9)
	##Account number- foreign key of Account model
    account_number = models.ForeignKey(Account)
	##Cheque Status type: chat
    status = models.CharField(max_length=30)
    def __unicode__(self):
        return self.cheque_number

##This is used to create Cheque Book table in the database to store cheque book information
class ChequeBook(models.Model):
	##Account number- foreign key of Account model
    account_number = models.ForeignKey(Account)
	##Size of the cheque book type: int
    size = models.IntegerField(max_length=11)
	##Issue date of cheque, type: date
    issue_date = models.DateField('issue date')
	##Starting cheque number type: int
    first_cheque_number = models.IntegerField(max_length=6)
    def __unicode__(self):
        return self.account_number_id

##This is used to create Employee table in the database to store employee information
class Employee(models.Model):
	##Employee id for authentication type: char
    employee_id = models.CharField(max_length=50)
	##Employee name type: char
    name = models.CharField(max_length=50)
	##Password for authentication type: char
    password = models.CharField(max_length=50)
    def __unicode__(self):
        return self.employee_id

##This is used to create Customer table in the database to store customer information
class Customer(models.Model):
	##Customer name type: char
    name = models.CharField(max_length=50)
	##Username of customer for authentication type: char
    username = models.CharField(max_length=50)
	## Password for authentication type: char
    password = models.CharField(max_length=50)
	##Account number of the customer type: char
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
    






