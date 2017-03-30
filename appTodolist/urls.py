from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.get_tasks, name="get_tasks"),
    url(r'^add$', views.add_task, name="add_task"),
    url(r'^set-done$', views.set_done_task, name="set_done_task"),
]