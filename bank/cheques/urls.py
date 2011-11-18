from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('cheques.views',
    (r'^$', 'login'),
	(r'^employeeLogin/$', 'employeeLogin'),
	(r'^employeeLogin/e_searchAccount/$', 'e_searchAccount'),
	(r'^customerLogin/$', 'customerLogin'),
	#(r'^customerLogin/c_searchAccount$', 'c_searchAccount'),
	(r'^customerMenu/$', 'customerMenu'),
	(r'^customerMenu/logoutCustomer/$', 'logoutCustomer'),
	(r'^customerMenu/c_chequeCancellation/$', 'c_chequeCancellation'),
	(r'^customerMenu/c_chequeStatus/$', 'c_chequeStatus'),
	(r'^employeeMenu/$', 'employeeMenu'),
	(r'^employeeMenu/e_chequePayment/$', 'e_chequePayment'),
	(r'^employeeMenu/e_issueChequeBook/$', 'e_issueChequeBook'),
	(r'^employeeMenu/e_chequeCancellation/$', 'e_chequeCancellation'),
	(r'^employeeMenu/e_chequeStatus/$', 'e_chequeStatus'),
	(r'^employeeMenu/logoutEmployee/$', 'logoutEmployee'),
)



	
