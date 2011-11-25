from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import ChequeHandler
from piston.doc import documentation_view 

cheque_payment = Resource(ChequeHandler)

urlpatterns = patterns( '',
	url(r'^bank/(?P<account_number>\d+)/(?P<cheque_number>\d+)/$', cheque_payment),
)
