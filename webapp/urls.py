from django.urls import path

from webapp import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('holidays', views.holidays, name='holidays'),
    path('add-holiday', views.add_holiday, name='add_holiday'),
    path('edit-holiday<int:hldy_id>', views.edit_holiday, name='edit_holiday'),
    path('employees', views.employees, name='employees'),
    path('add-employee', views.add_employee, name='add_employee'),
    path('edit-employee<int:emp_id>', views.edit_employee, name='edit_employee'),
    path('teams', views.teams, name='teams'),
    path('add-team', views.add_team, name='add_team'),
    path('edit-team<int:team_id>', views.edit_team, name='edit_team'),
    path('tasks', views.tasks, name='tasks'),
    path('add-tasks', views.add_tasks, name='add_tasks'),
    path('preliminary-verification<int:req_id>', views.preliminary_verification, name='preliminary_verification'),
    path('dharani-details-entry<int:task_id>', views.dharani_details_entry, name='dharani_details_entry'),
    path('prohibited-details-entry<int:task_id>', views.prohibited_details_entry, name='prohibited_details_entry'),
    path('encumbrance-details-entry<int:task_id>', views.encumbrance_details_entry, name='encumbrance_details_entry'),
    path('urbanland-details-entry<int:task_id>', views.urbanland_details_entry, name='urbanland_details_entry'),
    path('legalcase-details-entry<int:task_id>', views.legalcase_details_entry, name='legalcase_details_entry'),
]