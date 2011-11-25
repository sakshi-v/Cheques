from cheques.models import Account, Cheque, ChequeBook, Employee, Customer, Transaction
import datetime
from datetime import timedelta
from django.forms.fields import DateField, TimeField, ChoiceField, MultipleChoiceField
from django import forms
from django.forms.widgets import RadioSelect



## Creates a cheque payment form with the fields:cheque number - six digit number present on the cheque,amount - Amount present on the cheque,cheque date - Date present on the cheque,payee name - Payee name present on the cheque, 
class ChequePaymentForm(forms.Form):
	cheque_number=forms.IntegerField()
	amount=forms.DecimalField(max_digits=50, decimal_places=2)
	cheque_date=forms.DateField(widget=forms.TextInput(attrs={'size':'8'}))
	payee_name=forms.CharField()


## Creates a Employee login form with the following fields:employee id - Id of the employee, password -password of the employee
class EmployeeLoginForm(forms.Form):
	employee_id = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput())

## Creates a Customer login form with the following fields: customer id - Id of the employee, password -password of the employee
class CustomerLoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput())


## Creates a form for searching account number with the following field: Enter Account number - Account number of the drawee 
class SearchAccountNumberForm(forms.Form):
	account_number = forms.CharField(max_length=50)


## Choices for size of cheque book
SIZE_CHOICES = (('20', 20), ('50', 50))

## Creates a cheque book issue form with the radio field:size - choices 20 and 50

class IssueChequeBookForm(forms.Form):
	size=ChoiceField(widget=RadioSelect, choices=SIZE_CHOICES)
	value1=datetime.date.today()
	issueDate=DateField(initial=value1, widget=forms.widgets.HiddenInput())

## Creates a cheque cancellation form with the field:cheque number - six digit number present on the cheque
class ChequeCancellationForm(forms.Form):
	cheque_number=forms.IntegerField()

## Creates a cheque status form with the field: cheque number - six digit number present on the cheque
class ChequeStatusForm(forms.Form):
	cheque_number = forms.IntegerField()

