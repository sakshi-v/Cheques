from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from cheques.models import Account, Cheque, ChequeBook
import datetime
from datetime import timedelta
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django import forms
from django.forms.widgets import RadioSelect

accn=0

class ChequePaymentForm(forms.Form):
	cheque_number=forms.CharField(max_length=50)
	amount=forms.DecimalField(max_digits=50, decimal_places=2)
	cheque_date=forms.DateField(widget=forms.TextInput(attrs={'size':'8'}))
	payee_name=forms.CharField()

def chequePayment(request):
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
				return render_to_response('cheques/chequePayment.html', {
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
				return render_to_response('cheques/mainMenu.html', {
					'message': message,
					'form': sform
				}, context_instance=RequestContext(request))
			elif date>183:
				ch_info=Cheque(cheque_number=cheque_number, date=cheque_date, amount=amount,
							payee_name=payee_name, micr_number='500002023', account_number_id=acc_id, status='bounced')
				message="Cheque bounced due to expired date"
				ch_info.save()	
				return render_to_response('cheques/mainMenu.html', {
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
				return render_to_response('cheques/mainMenu.html', {
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
				
	return render_to_response('cheques/chequePayment.html', {
		'name': name,
		'balance': balance,
		'form': form,
	}, context_instance=RequestContext(request))

class SearchAccountNumberForm(forms.Form):
	account_number = forms.CharField(max_length=50)

def index(request):
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
				return render_to_response('cheques/index.html', {
					'form': form,
					'error_message': "Invalid Account Number",
				}, context_instance=RequestContext(request))	
			else:
				return render_to_response('cheques/mainMenu.html', {'acc': n})
	else:
		form=SearchAccountNumberForm()
	return render_to_response('cheques/index.html', {
		'form': form			
    }, context_instance=RequestContext(request))

def mainMenu(request):
	return render_to_response('cheques/mainMenu.html', {'acc': accn})

SIZE_CHOICES = (('20', 20), ('50', 50))

class IssueChequeBookForm(forms.Form):
	size=ChoiceField(widget=RadioSelect, choices=SIZE_CHOICES)
	value1=datetime.date.today()
	issueDate=DateField(initial=value1, widget=forms.widgets.HiddenInput())
	
def issueChequeBook(request):
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
			num_ch_books=num_ch_books+1
			Account.objects.filter(account_number=accn).update(number_of_chequebooks=num_ch_books)
			message="Cheque Book Issued"
			return render_to_response('cheques/mainMenu.html', {'message': message})
	else:
		form=IssueChequeBookForm()
	return render_to_response('cheques/issueChequeBook.html', {
		'name': name,
		'balance': balance,
		'accnum': accn,
		'form': form			
    }, context_instance=RequestContext(request))

class ChequeCancellationForm(forms.Form):
	cheque_number=forms.IntegerField()
	
def chequeCancellation(request):
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
				return render_to_response('cheques/mainMenu.html', {
					'messagee': status,
					'messa': 1
				}, context_instance=RequestContext(request))
			elif m==1 or int(cheque_number) < cnum or int(cheque_number) > csize:
				return render_to_response('cheques/chequeCancellation.html', {
					'form': form,
					'name': name,
					'accnum': accn, 
					'message': "Invalid Cheque number",
				}, context_instance=RequestContext(request))
			else:
				ch_info=Cheque(cheque_number=cheque_number, date=cheque_date, amount='000',
							micr_number='500002023', account_number_id=acc_id, status='cancelled')
				ch_info.save()
				return render_to_response('cheques/mainMenu.html', {
					'message': "Cheque has been cancelled",
				}, context_instance=RequestContext(request))
			
					
	else:
		form=ChequeCancellationForm()

	for num in Account.objects.all():
		a_num=num.account_number
		if accn==a_num:
			name=num.name
	return render_to_response('cheques/chequeCancellation.html', {
		'name': name,
		'accnum': accn, 
		'form': form,
		}, context_instance=RequestContext(request))

class ChequeStatusForm(forms.Form):
	cheque_number = forms.IntegerField()

def chequeStatus(request):
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
				return render_to_response('cheques/mainMenu.html', {'messag': status, 'mess': 1} )
			elif m==1 or int(cheque_number) < cnum or int(cheque_number) > csize:
				return render_to_response('cheques/chequeStatus.html', {
					'form': form,
					'error_message': "Invalid Cheque number",
				}, context_instance=RequestContext(request))
			else:
				return render_to_response('cheques/chequeStatus.html', {
					'form': form,
					'error_message': "Cheque hasn't received",
				}, context_instance=RequestContext(request))	
			
	else:
		form=ChequeStatusForm()
	return render_to_response('cheques/chequeStatus.html', {
		'form': form			
    }, context_instance=RequestContext(request))
