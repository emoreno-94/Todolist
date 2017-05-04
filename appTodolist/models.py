from __future__ import unicode_literals

from django.db import models


class TaskList(models.Model):
    name = models.TextField()
    priority = models.IntegerField(null=True)
    colour = models.CharField(max_length=8, default='#FFFFFF')

    def is_empty(self):
        return Task.objects.filter(task_list=self).count() < 1

    def add_task(self, new_task):
        self.task_set.add(new_task)
    
    def get_tasks(self):
        return self.task_set.order_by('done', '-priority')
    

class Task(models.Model):
    done = models.BooleanField(default=False)
    name = models.TextField()
    priority = models.BigIntegerField(null=True)
    task_list = models.ForeignKey(TaskList, null=True)

    def complete(self):
        self.done = True

    def change_state(self):
        self.done = not self.done

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            last = Task.objects.order_by("-priority").first()
            self.priority = last.priority + 1 if last else 1
        super(Task, self).save()

    def increase_priority(self):
        current_priority = self.priority
        to_swap = Task.objects.filter(priority__gt=self.priority, task_list=self.task_list).order_by("priority").first()
        if to_swap:
            self.priority = to_swap.priority
            to_swap.priority = current_priority
            to_swap.save()

    def decrease_priority(self):
        current_priority = self.priority
        to_swap = Task.objects.filter(priority__lt=self.priority, task_list=self.task_list).order_by("-priority").first()
        if to_swap:
            self.priority = to_swap.priority
            to_swap.priority = current_priority
            to_swap.save()
