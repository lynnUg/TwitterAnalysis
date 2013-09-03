from django.conf.urls.defaults import *
from mysite.views import hello, current_datetime, hours_ahead
from django.contrib import admin
admin.autodiscover()
from books import views
from blog import views as the_view
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    url(r'^hello/$', hello),
    url(r'^time/$', current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    (r'^admin/', include(admin.site.urls)),
    url(r'^search-form/$', views.search_form),
    url(r'^search/$', views.search),
    url(r'^contact/$', views.contact),
    url(r"^blog/", the_view.main),
    (r"^(\d+)/$", the_view.post),
    (r"^add_comment/(\d+)/$", the_view.add_comment),
)
