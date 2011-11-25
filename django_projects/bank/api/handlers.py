from piston.handler import BaseHandler
from cheques.models import Account, Cheque
from piston.doc import generate_doc

class ChequeHandler( BaseHandler ):
	allowed_methods = ('GET',)
	model = Account, Cheque 
	def read( self, request, account_number=0, cheque_number=0):
		if account_number:
			n=0
			for num in Account.objects.all():
				a_num=num.account_number
				if account_number==a_num:
					n=1
					name=num.name
			if n==0:
				return "Account doesn't exist"
			else:
				if cheque_number:	
					m=0	
					for num in Cheque.objects.all():
						a_num=num.cheque_number
						if cheque_number==a_num:
							m=1
							status=num.status	
					if m==0:	
						return "Invalid cheque number"
					else:	
						return "Cheque status: " + status
      
		
