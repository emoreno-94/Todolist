from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.get_tasks, name="get_tasks"),
    url(r'^add-task$', views.add_task, name="add_task"),
    url(r'^add-list$', views.add_list, name="add_list"),
    url(r'^change-state$', views.change_state_task, name="change_state"),
    url(r'^delete-task$', views.delete_task, name="delete_task"),
    url(r'^delete-list$', views.delete_list, name="delete_list"),
    url(r'^edit-name$', views.edit_name, name="edit_name"),
    url(r'^increase-priority-task$', views.increase_priority_task, name="increase_priority_task"),
    url(r'^decrease-priority-task$', views.decrease_priority_task, name="decrease_priority_task"),
    url(r'^increase-priority-list$', views.increase_priority_list, name="increase_priority_list"),
    url(r'^decrease-priority-list$', views.decrease_priority_list, name="decrease_priority_list"),
]