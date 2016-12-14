from django.conf.urls import url, patterns
import views as sendpdf_views

urlpatterns = patterns('',
                       url(r'^$', sendpdf_views.TemplateDesign.as_view(), name='design'),
                       url(r'^show/$', sendpdf_views.ShowDemo.as_view(), name='show'),
                       url(r'^download/$', sendpdf_views.DownloadDemo.as_view(), name='download'),
                       url(r'^send/$', sendpdf_views.SendDemo.as_view(), name='send'),)
