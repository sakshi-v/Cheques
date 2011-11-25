"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from django.test.client import Client
import unittest

from cheques.models import Account, ChequeBook, Cheque, Employee, Customer
from cheques.views import SearchAccountNumberForm, ChequePaymentForm, EmployeeLoginForm, CustomerLoginForm, IssueChequeBookForm, ChequeStatusForm
import datetime
from datetime import timedelta
from django.forms.fields import DateField, TimeField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect
try:
    from decimal import Decimal
except ImportError:
    from django.utils._decimal import Decimal

class NavigationTestCase(TestCase):
    
    def setUp(self):
        pass        
   
    def test_NavigationHome(self):
        """
        Checks whether all the pages are navigable or not.
        """
        c = Client()
        response = c.post('/cheques/')
        self.assertEqual(response.status_code, 200)

    def test_NavigationAccountSearch(self):
        
        c = Client()
        response = c.post('/cheques/employeeLogin/e_searchAccount/')
        self.assertEqual(response.status_code, 200)


    def test_ValidAccount(self):
        """
        Checks whether account number entered is valid.
        """
	account_number= '12345678'
        newAccount = Account.objects.create(account_number= '12345678', balance= '5000', name='sakshi', number_of_chequebooks='1')
        
        c = Client()
        response = c.post('/cheques/employeeLogin/e_searchAccount/',{'account_number':'12345678'})
        self.assertEqual(response.status_code,200)

    def test_invalid_accountnumber(self):
        
        resp = self.client.post('/cheques/employeeLogin/e_searchAccount/',{'account_number':'1234321'})
        self.assertEqual(resp.status_code, 200)
	
        self.assertEqual(resp.context['error_message'], "Invalid Account Number")


    def test_ChequePayment(self):
       
	first_cheque_number= 100477
	acc_n=30446461991
	newAccount = Account.objects.create(account_number= '30446461991', account_type='savings', balance= Decimal("5000.00"), name='sakshi', number_of_chequebooks=1)
        newChequeBook = ChequeBook.objects.create(account_number=newAccount, size=20, issue_date= '2010-10-10', first_cheque_number= first_cheque_number)
        c = Client()
	response = c.post('/cheques/employeeMenu/e_chequePayment/?account_number=30446461991',{'cheque_number':first_cheque_number, 'amount':Decimal("1000.00"), 'cheque_date':'2011-11-21', 'payee_name':'xyz'})
	for num in Cheque.objects.all():
		a_num=num.cheque_number
		if first_cheque_number==a_num:
			cheque_status=num.status
	self.assertEqual(cheque_status,'processed')       
	self.assertEqual(response.status_code,200)
	
    def test_invalid_Chequenumber_payment(self):

	first_cheque_number= 100477
	acc_n=30446461991
	newAccount = Account.objects.create(account_number= '30446461991', account_type='savings', balance= Decimal("5000.00"), name='sakshi', number_of_chequebooks=1)
        newChequeBook = ChequeBook.objects.create(account_number=newAccount, size=20, issue_date= '2010-10-10', first_cheque_number= first_cheque_number)
        c = Client()
	response = c.post('/cheques/employeeMenu/e_chequePayment/?account_number=30446461991',{'cheque_number':11212122, 'amount':Decimal("1000.00"), 'cheque_date':'2011-11-21', 'payee_name':'xyz'})
       	self.assertEqual(response.context['message'], "Invalid cheque number")
        self.assertEqual(response.status_code,200)

    def test_insufficient_balance_payment(self):

	first_cheque_number= 100477
	acc_n=30446461991
	newAccount = Account.objects.create(account_number= '30446461991', account_type='savings', balance= Decimal("5000.00"), name='sakshi', number_of_chequebooks=1)
        newChequeBook = ChequeBook.objects.create(account_number=newAccount, size=20, issue_date= '2010-10-10', first_cheque_number= first_cheque_number)
        c = Client()
	response = c.post('/cheques/employeeMenu/e_chequePayment/?account_number=30446461991',{'cheque_number':first_cheque_number, 'amount':Decimal("100000000000.00"), 'cheque_date':'2011-11-21', 'payee_name':'xyz'})
       	self.assertEqual(response.context['message'], "Cheque bounced due to insufficient balance")
        self.assertEqual(response.status_code,200)

    def test_date_expired_payment(self):

	first_cheque_number= 100477
	acc_n=30446461991
	newAccount = Account.objects.create(account_number= '30446461991', account_type='savings', balance= Decimal("5000.00"), name='sakshi', number_of_chequebooks=1)
        newChequeBook = ChequeBook.objects.create(account_number=newAccount, size=20, issue_date= '2010-10-10', first_cheque_number= first_cheque_number)
        c = Client()
	response = c.post('/cheques/employeeMenu/e_chequePayment/?account_number=30446461991',{'cheque_number':first_cheque_number, 'amount':Decimal("1000.00"), 'cheque_date':'2010-11-21', 'payee_name':'xyz'})
       	self.assertEqual(response.context['message'], "Cheque bounced due to expired date")
        self.assertEqual(response.status_code,200)

    def test_ChequeCancellation(self):

	from cheques.views import ChequeCancellationForm
       
	first_cheque_number= 111113
	newAccount = Account.objects.create(account_number= '30446461991', balance= 5000, name='sakshi', number_of_chequebooks=1)
        newChequeBook = ChequeBook.objects.create(account_number=newAccount, size=20, issue_date= '2011-11-11', first_cheque_number= first_cheque_number)
	cheque_number= 111113
	c = Client()
        response = c.post('/cheques/employeeMenu/e_chequeCancellation/?account_number=30446461991',{'cheque_number':cheque_number})
	for num in Cheque.objects.all():
		a_num=num.cheque_number
		if cheque_number==a_num:
			cheque_status=num.status
	
	self.assertEqual(cheque_status,'cancelled')
        self.assertEqual(response.status_code,200)

    def test_invalid_Chequenumber_cancellation(self):

	from cheques.views import ChequeCancellationForm
       
	first_cheque_number= 111113
	newAccount = Account.objects.create(account_number= '30446461991', balance= 5000, name='sakshi', number_of_chequebooks=1)
        newChequeBook = ChequeBook.objects.create(account_number=newAccount, size=20, issue_date= '2011-11-11', first_cheque_number= first_cheque_number)
	cheque_number= 111211
	c = Client()
        response = c.post('/cheques/employeeMenu/e_chequeCancellation/?account_number=30446461991',{'cheque_number':cheque_number})
	self.assertEqual(response.context['message'], "Invalid Cheque number")
        self.assertEqual(response.status_code,200)

    def test_IssueChequeBook(self):
       	account_number='30446461991'
	newAccount = Account.objects.create(account_number= '30446461991', balance= 5000, name='sakshi', number_of_chequebooks=0)
        first_cheque_number=111111
	c = Client()
	
        response = c.post('/cheques/employeeMenu/e_issueChequeBook/?account_number=30446461991',{'size': 20})
	cb_size=0
	for num in ChequeBook.objects.all():
		a_num=num.account_number_id
		if account_number=='30446461991':
			cb_size=num.size
	
	self.assertEqual(response.status_code,200)
      
    def test_valid_employeelogin(self):
	newEmployee = Employee.objects.create(employee_id= '123', name='sakshi', password="verma")
	c = Client()
	
        response = c.post('/cheques/employeeLogin/',{'employee_id': '123', 'password': 'verma'})
	self.assertEqual(response.status_code,200)
	

    def test_invalid_employeelogin(self):
	newEmployee = Employee.objects.create(employee_id= '123', name='sakshi', password="verma")
	c = Client()
	
        response = c.post('/cheques/employeeLogin/',{'employee_id': '12321', 'password': 'verma'})
	
	self.assertEqual(response.context['error_message'], "Invalid ID or Password")
        self.assertEqual(response.status_code,200)
     
    def test_valid_customerlogin(self):
	newAccount = Account.objects.create(account_number= '30446461991', balance= 5000, name='sakshi', number_of_chequebooks=0)
	newCustomer = Customer.objects.create(username= '123', name='sakshi', password="verma", account_number=newAccount)
	c = Client()
	
        response = c.post('/cheques/customerLogin/',{'username': '123', 'password': 'verma'})
	self.assertEqual(response.status_code,200)
	

    def test_invalid_customerlogin(self):
	newAccount = Account.objects.create(account_number= '30446461991', balance= 5000, name='sakshi', number_of_chequebooks=0)
	newCustomer = Customer.objects.create(username= '123', name='sakshi', password="verma", account_number=newAccount)
	c = Client()
	
        response = c.post('/cheques/customerLogin/',{'username': '123', 'password': 'sakshi'})
	
	self.assertEqual(response.context['error_message'], "Invalid username or password")
        self.assertEqual(response.status_code,200)   


