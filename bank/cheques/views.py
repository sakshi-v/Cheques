from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from cheques.models import Account, Cheque, ChequeBook, Employee, Customer, Transaction
import datetime
from datetime import timedelta
from django.forms.fields import DateField, TimeField, ChoiceField, MultipleChoiceField
from django import forms
from django.forms.widgets import RadioSelect

accn=0
e_id=0

class ChequePaymentForm(forms.Form):
	cheque_number=forms.CharField(max_length=50)
	amount=forms.DecimalField(max_digits=50, decimal_places=2)
	cheque_date=forms.DateField(widget=forms.TextInput(attrs={'size':'8'}))
	payee_name=forms.CharField()

def e_chequePayment(request):
	if request.method == 'POST':
		form = ChequePaymentForm(request.POST)
		if form.is_valid():
			global accn
			cheque_number = form.cleaned_data['cheque_number']
			amount = form.cleaned_data['amount']
			cheque_date = form.cleaned_data['cheque_date']
			payee_name = form.cleaned_data['payee_name']
			today_date=datetime.date.today()
			date = today_date-cheque_date	
			date=date.days
			acc_id=0
			for num in Account.objects.all():
				a_num=num.account_number
				if accn==a_num:
					name=num.name
					balance=num.balance
					acc_id=num.id
			
			m=0
			for cn in Cheque.objects.all():
				a_cn=cn.cheque_number
				if cheque_number==a_cn:
					m=1
			sform=SearchAccountNumberForm()
			cb=ChequeBook.objects.get(account_number=acc_id)		
			cnum=cb.first_cheque_number
			csize=cb.size + cnum
			if m==1 or int(cheque_number) < cnum or int(cheque_number) > csize:
				return render_to_response('cheques/e_chequePayment.html', {
					'name': name,
					'balance': balance,
					'form': form,
					'message': "Invalid cheque number"
				}, context_instance=RequestContext(request))
			if balance<amount:
				ch_info=Cheque(cheque_number=cheque_number, date=cheque_date, amount=amount,
							payee_name=payee_name, micr_number='500002023', account_number_id=acc_id, status='bounced')
				message="Cheque bounced due to insufficient balance"
				ch_info.save()	
				return render_to_response('cheques/employeeMenu.html', {
					'message': message,
					'form': sform
				}, context_instance=RequestContext(request))
			elif date>183:
				ch_info=Cheque(cheque_number=cheque_number, date=cheque_date, amount=amount,
							payee_name=payee_name, micr_number='500002023', account_number_id=acc_id, status='bounced')
				message="Cheque bounced due to expired date"
				ch_info.save()	
				return render_to_response('cheques/employeeMenu.html', {
					'message': message,
					'form': sform
				}, context_instance=RequestContext(request))
			else:
				balance=balance-amount
				Account.objects.filter(account_number=accn).update(balance=balance)
				ch_info=Cheque(cheque_number=cheque_number, date=cheque_date, amount=amount,
							payee_name=payee_name, micr_number='500002023', account_number_id=acc_id, status='processed')
				message="Cheque processed successfully"	
				ch_info.save()		
				return render_to_response('cheques/employeeMenu.html', {
					'message': message,
					'form': sform
				}, context_instance=RequestContext(request))
			
	else:
		form=ChequePaymentForm()

	for num in Account.objects.all():
		a_num=num.account_number
		if accn==a_num:
			name=num.name
			balance=num.balance
				
	return render_to_response('cheques/e_chequePayment.html', {
		'name': name,
		'balance': balance,
		'form': form,
	}, context_instance=RequestContext(request))

class EmployeeLoginForm(forms.Form):
	employee_id = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput())

def employeeLogin(request):
	if request.method == 'POST':
		form = EmployeeLoginForm(request.POST)
		form1 = SearchAccountNumberForm();
		if form.is_valid():
			employee_id = form.cleaned_data['employee_id']
			password = form.cleaned_data['password']
			global e_id
			n=0
			empId=employee_id
			passw=password
			for num in Employee.objects.all():
				emp_id=num.employee_id
				passwrd=num.password
				if empId==emp_id and passw==passwrd:
					n=empId
					e_id=n
					break
			if n==0:
				return render_to_response('cheques/employeeLogin.html', {
					'form': form,
					'error_message': "Invalid ID or Password",
				}, context_instance=RequestContext(request))	
			else:
				return render_to_response('cheques/e_searchAccount.html', {'form': form1
				},  context_instance=RequestContext(request))
	else:
		form=EmployeeLoginForm()
	return render_to_response('cheques/employeeLogin.html', {
		'form': form			
    }, context_instance=RequestContext(request))

class CustomerLoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput())

def customerLogin(request):
	if request.method == 'POST':
		form = CustomerLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			global accn
			n=0
			user_name=username
			passw=password
			for num in Customer.objects.all():
				user=num.username
				passwrd=num.password
				if user==user_name and passw==passwrd:
					n=num.account_number
					break
			accn = n
			acc_n=Account.objects.get(account_number=accn)		
			name=acc_n.name
			if n==0:
				return render_to_response('cheques/customerLogin.html', {
					'form': form,
					'error_message': "Invalid username or password",
				}, context_instance=RequestContext(request))	
			else:
				return render_to_response('cheques/customerMenu.html', {'name': name})
	else:
		form=CustomerLoginForm()
	return render_to_response('cheques/customerLogin.html', {
		'form': form			
    }, context_instance=RequestContext(request))

class SearchAccountNumberForm(forms.Form):
	account_number = forms.CharField(max_length=50)

def e_searchAccount(request):
	if request.method == 'POST':
		form = SearchAccountNumberForm(request.POST)
		if form.is_valid():
			account_number = form.cleaned_data['account_number']
			global accn
			n=0
			accNum=account_number
			for num in Account.objects.all():
				a_num=num.account_number
				if accNum==a_num:
					n=accNum
					accn=n
					break
			if n==0:
				return render_to_response('cheques/e_searchAccount.html', {
					'form': form,
					'error_message': "Invalid Account Number",
				}, context_instance=RequestContext(request))	
			else:
				return render_to_response('cheques/employeeMenu.html', {'acc': n})
	else:
		form=SearchAccountNumberForm()
	return render_to_response('cheques/e_searchAccount.html', {
		'form': form			
	}, context_instance=RequestContext(request))

def employeeMenu(request):
	return render_to_response('cheques/employeeMenu.html', {'acc': accn})

def logoutCustomer(request):
	global accn
	accn=0
	return render_to_response('cheques/login.html')

def logoutEmployee(request):
	global accn
	accn=0
	return render_to_response('cheques/login.html')

def customerMenu(request):
	global accn
	acc_nu=Account.objects.get(account_number=accn)		
	name=acc_nu.name
	return render_to_response('cheques/customerMenu.html', {'name': name})

def login(request):
	return render_to_response('cheques/login.html')

SIZE_CHOICES = (('20', 20), ('50', 50))

class IssueChequeBookForm(forms.Form):
	size=ChoiceField(widget=RadioSelect, choices=SIZE_CHOICES)
	value1=datetime.date.today()
	issueDate=DateField(initial=value1, widget=forms.widgets.HiddenInput())
	
def e_issueChequeBook(request):
	for num in Account.objects.all():
		a_num=num.account_number
		if accn==a_num:
			name=num.name
			balance=num.balance
			acc_id=num.id
			num_ch_books=num.number_of_chequebooks
	if request.method == 'POST':
		form = IssueChequeBookForm(request.POST)
		if form.is_valid():
			size=form.cleaned_data['size']
			issueDate=form.cleaned_data['issueDate']
			today_date=issueDate
			if num_ch_books==0:
				first_ch_num=100000
				ch_book=ChequeBook(account_number_id=acc_id, size=int(size), issue_date=today_date, first_cheque_number=first_ch_num)
				ch_book.save()
			else:
				fch=0
				fnum=ChequeBook.objects.get(account_number=acc_id)
				fch=fnum.first_cheque_number
				first_ch_num=fch+int(size)
				ChequeBook.objects.filter(account_number=acc_id).update(account_number=acc_id, 
							size=size, issue_date=today_date, first_cheque_number=first_ch_num)
			num_ch_books=int(num_ch_books)+1
			Account.objects.filter(account_number=accn).update(number_of_chequebooks=num_ch_books)
			message="Cheque Book Issued"
			return render_to_response('cheques/employeeMenu.html', {'message': message})
	else:
		form=IssueChequeBookForm()
	return render_to_response('cheques/e_issueChequeBook.html', {
		'name': name,
		'balance': balance,
		'accnum': accn,
		'form': form			
    }, context_instance=RequestContext(request))

class ChequeCancellationForm(forms.Form):
	cheque_number=forms.IntegerField()
	
def e_chequeCancellation(request):
	if request.method == 'POST':
		form = ChequeCancellationForm(request.POST)
		if form.is_valid():
			cheque_number = form.cleaned_data['cheque_number']
			global accn
			n=1
			acc_id=0
			for num in Account.objects.all():
				a_num=num.account_number
				if accn==a_num:
					acc_id=num.id
					name=num.name
			for num in Cheque.objects.all():
				ac_id=num.account_number_id
				c_num=num.cheque_number
				if int(cheque_number)==int(c_num) and int(acc_id)==int(ac_id):
					status=num.status
					n=cheque_number
					break	
			m=0
			for cn in Cheque.objects.all():
				a_cn=cn.cheque_number
				if cheque_number==a_cn:
					m=1
			cb=ChequeBook.objects.get(account_number=acc_id)		
			cnum=cb.first_cheque_number
			csize=cb.size + cnum
			cheque_date=datetime.date.today()
			if n!=1:
				return render_to_response('cheques/employeeMenu.html', {
					'messagee': status,
					'messa': 1
				}, context_instance=RequestContext(request))
			elif m==1 or int(cheque_number) < cnum or int(cheque_number) > csize:
				return render_to_response('cheques/e_chequeCancellation.html', {
					'form': form,
					'name': name,
					'accnum': accn, 
					'message': "Invalid Cheque number",
				}, context_instance=RequestContext(request))
			else:
				ch_info=Cheque(cheque_number=cheque_number, date=cheque_date, amount='000',
							micr_number='500002023', account_number_id=acc_id, status='cancelled')
				ch_info.save()
				return render_to_response('cheques/employeeMenu.html', {
					'message': "Cheque has been cancelled",
				}, context_instance=RequestContext(request))
			
					
	else:
		form=ChequeCancellationForm()

	for num in Account.objects.all():
		a_num=num.account_number
		if accn==a_num:
			name=num.name
	return render_to_response('cheques/e_chequeCancellation.html', {
				
		'name': name,
		'accnum': accn, 
		'form': form,
		}, context_instance=RequestContext(request))

class ChequeStatusForm(forms.Form):
	cheque_number = forms.IntegerField()

def e_chequeStatus(request):
	if request.method == 'POST':
		form = ChequeStatusForm(request.POST)
		if form.is_valid():
			cheque_number = form.cleaned_data['cheque_number']
			global accn
			n=1
			acc_id=0
			for num in Account.objects.all():
				a_num=num.account_number
				if accn==a_num:
					acc_id=num.id
			for num in Cheque.objects.all():
				ac_id=num.account_number_id
				c_num=num.cheque_number
				if int(cheque_number)==int(c_num) and int(acc_id)==int(ac_id):
					status=num.status
					n=cheque_number
					break	
			m=0
			for cn in Cheque.objects.all():
				a_cn=cn.cheque_number
				if cheque_number==a_cn:
					m=1
			cb=ChequeBook.objects.get(account_number=acc_id)		
			cnum=cb.first_cheque_number
			csize=cb.size + cnum
			if n!=1:
				return render_to_response('cheques/employeeMenu.html', {'messag': status, 'mess': 1} )
			elif m==1 or int(cheque_number) < cnum or int(cheque_number) > csize:
				return render_to_response('cheques/e_chequeStatus.html', {
					'form': form,
					'error_message': "Invalid Cheque number",
				}, context_instance=RequestContext(request))
			else:
				return render_to_response('cheques/e_chequeStatus.html', {
					'form': form,
					'error_message': "Cheque hasn't received",
				}, context_instance=RequestContext(request))	
			
	else:
		form=ChequeStatusForm()
	return render_to_response('cheques/e_chequeStatus.html', {
		'form': form			
    }, context_instance=RequestContext(request))



def c_chequeCancellation(request):
	if request.method == 'POST':
		form = ChequeCancellationForm(request.POST)
		if form.is_valid():
			cheque_number = form.cleaned_data['cheque_number']
			global accn
			n=1
			acc_id=0
			acc_nu=Account.objects.get(account_number=accn)		
			name=acc_nu.name
			acc_id=acc_nu.id
			for num in Cheque.objects.all():
				ac_id=num.account_number_id
				c_num=num.cheque_number
				if int(cheque_number)==int(c_num) and int(acc_id)==int(ac_id):
					status=num.status
					n=cheque_number
					break	
			m=0
			for cn in Cheque.objects.all():
				a_cn=cn.cheque_number
				if cheque_number==a_cn:
					m=1
			cb=ChequeBook.objects.get(account_number=acc_id)		
			cnum=cb.first_cheque_number
			csize=cb.size + cnum
			cheque_date=datetime.date.today()
			if n!=1:
				return render_to_response('cheques/customerMenu.html', {
					'messagee': status,
					'messa': 1,
					'name': name
				}, context_instance=RequestContext(request))
			elif m==1 or int(cheque_number) < cnum or int(cheque_number) > csize:
				return render_to_response('cheques/c_chequeCancellation.html', {
					'form': form,
					'name': name,
					'accnum': accn, 
					'message': "Invalid Cheque number",
				}, context_instance=RequestContext(request))
			else:
				ch_info=Cheque(cheque_number=cheque_number, date=cheque_date, amount='000',
							micr_number='500002023', account_number_id=acc_id, status='cancelled')
				ch_info.save()
				return render_to_response('cheques/customerMenu.html', {
					'message': "Cheque has been cancelled",
				}, context_instance=RequestContext(request))
			
					
	else:
		form=ChequeCancellationForm()
	acc_n=Account.objects.get(account_number=accn)		
	name=acc_n.name
	return render_to_response('cheques/c_chequeCancellation.html', {
		'name': name,		
		'accnum': accn, 
		'form': form,
		}, context_instance=RequestContext(request))


def c_chequeStatus(request):
	if request.method == 'POST':
		form = ChequeStatusForm(request.POST)
		if form.is_valid():
			cheque_number = form.cleaned_data['cheque_number']
			global accn
			n=1
			acc_id=0
			acc_nu=Account.objects.get(account_number=accn)		
			name=acc_nu.name
			acc_id=acc_nu.id
			for num in Cheque.objects.all():
				ac_id=num.account_number_id
				c_num=num.cheque_number
				if int(cheque_number)==int(c_num) and int(acc_id)==int(ac_id):
					status=num.status
					n=cheque_number
					break	
			m=0
			for cn in Cheque.objects.all():
				a_cn=cn.cheque_number
				if cheque_number==a_cn:
					m=1
			cb=ChequeBook.objects.get(account_number=acc_id)		
			cnum=cb.first_cheque_number
			csize=cb.size + cnum
			if n!=1:
				return render_to_response('cheques/customerMenu.html', {'messag': status, 'mess': 1, 'name': name} )
			elif m==1 or int(cheque_number) < cnum or int(cheque_number) > csize:
				return render_to_response('cheques/c_chequeStatus.html', {
					'form': form,
					'error_message': "Invalid Cheque number",
				}, context_instance=RequestContext(request))
			else:
				return render_to_response('cheques/c_chequeStatus.html', {
					'form': form,
					'error_message': "Cheque hasn't received",
				}, context_instance=RequestContext(request))	
			
	else:
		form=ChequeStatusForm()
	return render_to_response('cheques/c_chequeStatus.html', {
		'form': form			
    }, context_instance=RequestContext(request))


