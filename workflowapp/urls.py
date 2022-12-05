from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('create_employee', views.create_employee),
    path('employee', views.employee),
    path('holiday', views.holiday),
    path('team', views.team),
    path('get-employee', views.getEmployee),
    path('save-preliminarytask', views.save_preliminary_task),
    path('save-image', views.save_image),
    path('get-screens', views.get_screens),
    path('delete-screen', views.delete_screen),
    path('save-dharani-details', views.save_dharani_details),
    path('save-preliminary-details', views.save_preliminary_details),
    path('save-encumbrance-details', views.save_encumbrance_details),
    path('save-urban-details', views.save_urbanland_details),
    path('save-legalcase-details', views.save_legalcase_details),
]