from django.test import TestCase, Client
from appTodolist.models import Task, TaskList


class TodoTest (TestCase):

    def test_empty(self):
        # arrange
        t = TaskList()
        # act
        # assert
        self.assertTrue(t.is_empty())
    
    def test_get_empty(self):
        # arrange
        t = TaskList()
        # act
        # assert
        self.assertTrue(len(t.get_tasks()) == 0)

    def test_add_task(self):
        # arrange
        tasks_list = TaskList.objects.create(name='test')
        task = Task.objects.create(name="name!!")
        # act
        tasks_list.add_task(task)
        tasks_list.save()

        task_list_db = TaskList.objects.get(pk=tasks_list.id)
        # assert
        self.assertFalse(task_list_db.is_empty())
    
    def test_list(self):
        # arrange
        task_list = TaskList.objects.create(name="Lista")
        
        task1 = Task.objects.create(name="Tarea1")
        task_list.add_task(task1)
        
        task2 = Task.objects.create(name="Tarea2")
        task_list.add_task(task2)

        task_list.save()

        # act
        t_list = TaskList.objects.get(pk=task_list.id).get_tasks()
        # assert
        self.assertTrue(task1 in t_list)
        self.assertTrue(task2 in t_list)
        

class TasksTest (TestCase):

    def test_name(self):
        # arrange
        name = "Name"
        task = Task.objects.create(name=name)
        # act
        task_db = Task.objects.get(pk=task.id)
        # assert
        self.assertEquals(name, task_db.name)

    def test_pending(self):
        # arrange
        name = "name"
        task = Task.objects.create(name=name)
        # act
        task_db = Task.objects.get(pk=task.id)
        # assert
        self.assertFalse(task_db.done)

    def test_change_state(self):
        # arrange
        name = "name"
        task = Task.objects.create(name=name)
        # act
        prev_state = task.done
        task.change_state()
        task.save()
        task_db = Task.objects.get(pk=task.id)
        curr_state = task_db.done
        task_db.change_state()
        task_db.save()
        task_db = Task.objects.get(pk=task.id)
        # assert
        self.assertFalse(prev_state)
        self.assertTrue(curr_state)
        self.assertFalse(task_db.done)

    def test_char_limit(self):
        # arrange
        long_ass_name = "loong"*10
        task = Task.objects.create(name=long_ass_name)
        #act
        db_task = Task.objects.get(pk=task.id)
        # assert
        self.assertEquals(long_ass_name, db_task.name)

    def test_priority(self):
        # arrange
        task_list = TaskList.objects.create(name="listy")
        task1 = Task.objects.create(name="test1", task_list=task_list)
        task2 = Task.objects.create(name="test2", task_list=task_list)
        #act
        db_task1 = Task.objects.get(pk=task1.id)
        db_task2 = Task.objects.get(pk=task2.id)
        # assert
        self.assertEquals(1, db_task1.priority)
        self.assertEquals(2, db_task2.priority)

    def test_increase_priority(self):
        # arrange
        task_list = TaskList.objects.create(name="listy")
        task_list2 = TaskList.objects.create(name="notListy")
        task1 = Task.objects.create(name="test1", task_list=task_list)
        task_from_another_list = Task.objects.create(name="the namest", task_list=task_list2)
        task2 = Task.objects.create(name="test2", task_list=task_list)
        #act
        task1.increase_priority()
        task1.save()
        db_task1 = Task.objects.get(pk=task1.id)
        db_task_from_another_list = Task.objects.get(pk=task_from_another_list.id)
        db_task2 = Task.objects.get(pk=task2.id)
        # assert
        self.assertEquals(3, db_task1.priority)
        self.assertEquals(2, db_task_from_another_list.priority)
        self.assertEquals(1, db_task2.priority)

    def test_decrease_priority(self):
        # arrange
        task_list = TaskList.objects.create(name="Listy")
        task_list2 = TaskList.objects.create(name="notListy")
        task1 = Task.objects.create(name="test1", task_list=task_list)
        task_from_another_list = Task.objects.create(name="the namest", task_list=task_list2)
        task2 = Task.objects.create(name="test2", task_list=task_list)
        #act
        task2.decrease_priority()
        task2.save()
        db_task1 = Task.objects.get(pk=task1.id)
        db_task_from_another_list = Task.objects.get(pk=task_from_another_list.id)
        db_task2 = Task.objects.get(pk=task2.id)
        # assert
        self.assertEquals(3, db_task1.priority)
        self.assertEquals(2, db_task_from_another_list.priority)
        self.assertEquals(1, db_task2.priority)


class TaskViewTest(TestCase):
    def test_view_task(self):
        # arrange
        client = Client()
        # act
        get_response = client.get('/tasks/')
        post_response = client.post('/tasks/')
        # assert
        self.assertEquals(200, get_response.status_code)
        self.assertEquals(405, post_response.status_code)

    def test_render_html_view_task(self):
        # arrange
        client = Client()
        context = {
            'task_lists': Task.objects.all()
        }
        # act
        response = client.get('/tasks/')
        # assert
        self.assertEquals(list(context['task_lists']), list(response.context['task_lists']))

    def test_connection_add_list(self):
        # arrange
        client = Client()
        # act
        get_response = client.get('/tasks/add-list')
        post_response = client.post('/tasks/add-list')
        # assert
        self.assertEquals(405, get_response.status_code)
        self.assertEquals(302, post_response.status_code)

    def test_view_add_list(self):
        # arrange
        client = Client()
        form = {
            'name': 'Test',
        }
        # act
        post_response = client.post('/tasks/add-list', form)
        # assert
        list_db = TaskList.objects.filter(name='Test').first()
        self.assertIsNotNone(list_db)

    def test_connection_add_task(self):
        # arrange
        client = Client()
        # act
        get_response = client.get('/tasks/add-task')
        post_response = client.post('/tasks/add-task')
        # assert
        self.assertEquals(405, get_response.status_code)
        self.assertEquals(302, post_response.status_code)

    def test_view_add_task(self):
        # arrange
        task_list = TaskList.objects.create(name="listy")
        client = Client()
        form = {
            'task_name': 'Test',
            'list_id': task_list.id
        }
        # act
        post_response = client.post('/tasks/add-task', form)
        # assert
        task_db = Task.objects.filter(name='Test', task_list=task_list).first()
        self.assertIsNotNone(task_db)

    def test_connection_change_state(self):
        # arrange
        client = Client()
        # act
        get_response = client.get('/tasks/change-state')
        post_response = client.post('/tasks/change-state')
        # assert
        self.assertEquals(405, get_response.status_code)
        self.assertEquals(302, post_response.status_code)

    def test_view_change_state(self):
        # arrange
        client = Client()
        task = Task(name="namename")
        task.save()
        state_prev = task.done
        # act
        post_response = client.post('/tasks/change-state', {"id": task.id})
        task = Task.objects.filter(name="namename").first()
        # assert
        self.assertNotEquals(state_prev, task.done)

    def test_view_change_state_invalid_id(self):
        # arrange
        client = Client()
        # act
        post_response = client.post('/tasks/change-state', {'id': 1})
        # assert
        self.assertEquals(404, post_response.status_code)

    def test_connection_delete_task(self):
        # arrange
        client = Client()
        # act
        get_response = client.get('/tasks/delete')
        post_response = client.post('/tasks/delete')
        # assert
        self.assertEquals(405, get_response.status_code)
        self.assertEquals(302, post_response.status_code)

    def test_view_delete_task(self):
        # arrange
        client = Client()
        task = Task(name='namename')
        task.save()
        # act
        post_response = client.post('/tasks/delete', {'id': task.id})
        # assert
        self.assertRaises(Task.DoesNotExist, Task.objects.get, pk=task.id)

    def test_connection_edit_name_task(self):
        # arrange
        client = Client()
        # act
        get_response = client.get('/tasks/edit-name')
        post_response = client.post('/tasks/edit-name')
        # assert
        self.assertEquals(405, get_response.status_code)
        self.assertEquals(302, post_response.status_code)

    def test_view_edit_name(self):
        # arrange
        client = Client()
        pre_name = 'name'
        post_name = 'post'
        task = Task(name=pre_name)
        task.save()
        # act
        post_response = client.post('/tasks/edit-name', {'id': task.id, 'name': post_name})
        task = Task.objects.get(pk=task.id)
        # assert
        self.assertEquals(post_name, task.name)

    def test_connection_increase_priority_task(self):
        # arrange
        client = Client()
        # act
        get_response = client.get('/tasks/increase-priority')
        post_response = client.post('/tasks/increase-priority')
        # assert
        self.assertEquals(405, get_response.status_code)
        self.assertEquals(302, post_response.status_code)

    def test_view_increase_priority(self):
        # arrange
        client = Client()
        task1 = Task.objects.create(name="task1")
        task2 = Task.objects.create(name="task2")
        # act
        post_response = client.post('/tasks/increase-priority', {'id': task1.id})
        save_task = Task.objects.get(pk=task1.id)
        # assert
        self.assertEquals(save_task.priority, 2)

    def test_connection_decrease_priority_task(self):
        # arrange
        client = Client()
        # act
        get_response = client.get('/tasks/decrease-priority')
        post_response = client.post('/tasks/decrease-priority')
        # assert
        self.assertEquals(405, get_response.status_code)
        self.assertEquals(302, post_response.status_code)

    def test_view_decrease_priority(self):
        # arrange
        client = Client()
        task1 = Task.objects.create(name="task1")
        task2 = Task.objects.create(name="task2")
        # act
        post_response = client.post('/tasks/decrease-priority', {'id': task2.id})
        save_task = Task.objects.get(pk=task2.id)
        # assert
        self.assertEquals(save_task.priority, 1)