"""URL conf for the app"""
# pylint: disable=invalid-name
from django.urls import path
from . import views as sendpdf_views

urlpatterns = [
    path('', sendpdf_views.TemplateDesign.as_view(), name='design'),
    path('show/', sendpdf_views.ShowDemo.as_view(), name='show'),
    path('download/', sendpdf_views.DownloadDemo.as_view(), name='download'),
    path('send/', sendpdf_views.SendDemo.as_view(), name='send'),
]
