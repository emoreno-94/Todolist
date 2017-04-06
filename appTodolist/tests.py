from django.test import TestCase, Client
from appTodolist.models import Task, TaskList
from django.template import loader


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
        '''
        add task, is empty,
        '''
        # arrange
        tasks_list = TaskList()
        tasks_list.save()
        task = Task(name="name!!")
        task.save()
        #act
        tasks_list.add_task(task)
        # assert
        self.assertFalse(tasks_list.is_empty())
    
    def test_list(self):
        # arrange
        task_list = TaskList(name="Lista")
        task_list.save()
        
        task1 = Task(name="Tarea1") 
        task1.save()
        task_list.add_task(task1)
        
        task2 = Task(name="Tarea2") 
        task2.save()
        task_list.add_task(task2)
        
        # act
        t_list = task_list.get_tasks()
        # assert
        self.assertTrue(task1 in t_list)
        self.assertTrue(task2 in t_list)
        

class TasksTest (TestCase):

    def test_name(self):
        # arrange
        name = "Name"
        task = Task(name=name)
        # act
        # assert
        self.assertEquals(name, task.name)

    def test_pending(self):
        # arrange
        task = Task(name="Name")
        # act
        # assert
        self.assertFalse(task.done)

    def test_change_state(self):
        # arrange
        task = Task(name="Name")
        # act
        prev_state = task.done
        task.change_state()
        curr_state = task.done
        task.change_state()
        # assert
        self.assertFalse(prev_state)
        self.assertTrue(curr_state)
        self.assertFalse(task.done)

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
            'tasks': Task.objects.all()
        }
        # act
        response = client.get('/tasks/')
        template = loader.get_template('appTodoList/tasks.html')
        html = template.render(context)
        # assert
        self.assertEquals(html, response.content)

    def test_connection_add_task(self):
        # arrange
        client = Client()
        # act
        get_response = client.get('/tasks/add')
        post_response = client.post('/tasks/add')
        # assert
        self.assertEquals(405, get_response.status_code)
        self.assertEquals(302, post_response.status_code)

    def test_view_add_task(self):
        # arrange
        client = Client()
        task = {
            'name': 'Test'
        }
        # act
        post_response = client.post('/tasks/add', task)
        # assert
        task_db = Task.objects.filter(name='Test').first()
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