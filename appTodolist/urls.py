from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.get_tasks, name="get_tasks"),
    url(r'^add$', views.add_task, name="add_task"),
    url(r'^change-state', views.change_state_task, name="change_state"),
    url(r'^delete', views.delete_task, name="delete_task"),
    url(r'^edit-name', views.edit_name, name="edit_name"),
]