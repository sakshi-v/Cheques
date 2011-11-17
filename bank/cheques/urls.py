from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('cheques.views',
    (r'^$', 'index'),
    (r'^mainMenu/$', 'mainMenu'),
	(r'^mainMenu/chequePayment/$', 'chequePayment'),
	(r'^mainMenu/issueChequeBook/$', 'issueChequeBook'),
	(r'^mainMenu/chequeCancellation/$', 'chequeCancellation'),
	(r'^mainMenu/chequeStatus/$', 'chequeStatus'),
)
