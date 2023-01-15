from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='data-home'),
    path('visualizer/<str:data>', views.visualizer, name='visualizer'),
    path('relational-chart/<str:chart>', views.relational_chart, name='relational'),
    path('distribution_chart/<str:chart>', views.distribution_chart, name='distribution'),
    path('categorical_chart/<str:chart>', views.categorical_chart, name='categorical'),
    path('show_data', views.show_data, name='show_data'),
]
