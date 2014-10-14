from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import DetailView, ListView
from stockmarket.models import Investor
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'se2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$','stockmarket.views.index'),
	url(r'^startup/(?P<startup_id>\d+)/$','stockmarket.views.startup'),
    #url(r'^success/', 'stockmarket.views.success'),
	url(r'^logout/','stockmarket.views.logout'),
	url(r'^signin/','stockmarket.views.signin'),
	url(r'^signup/','stockmarket.views.signup'),
	url(r'^home/','stockmarket.views.home'),
	url(r'^validate-purchase/','stockmarket.views.validate_purchase'),
	url(r'^startup/edit/(?P<startup_id>\d+)/$','stockmarket.views.edit_startup'),
	url(r'^validate-price/','stockmarket.views.validate_price'),
	url(r'^my-portafolio/','stockmarket.views.my_portafolio'),
	url(r'^winner/','stockmarket.views.winner'),
	url(r'^fblogin/','stockmarket.views.fblogin'),
	url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
	

)

urlpatterns += staticfiles_urlpatterns()