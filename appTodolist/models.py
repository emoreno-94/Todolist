from __future__ import unicode_literals

from django.db import models

# Create your models here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class TaskList(models.Model):
    name = models.CharField(max_length=20)
    
    def is_empty(self):
        return Task.objects.filter(task_list=self).count() < 1
    
    def add_task(self, new_task):
        self.task_set.add(new_task)
    
    def get_tasks(self):
        return self.task_set.all()
    

class Task(models.Model):
    done = models.BooleanField(default=False)
    name = models.CharField(max_length=20)
    task_list = models.ForeignKey(TaskList, null=True)

    def complete(self):
        self.done = True

    def change_state(self):
        self.done = not self.done
