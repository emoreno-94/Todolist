from behave import given, when, then

from appTodolist.models import TaskList, Task


@given(u'I go to "{url}"')
def step_impl(context, url):
    list_db = TaskList.objects.create(name='list')
    Task.objects.create(name='task_1', task_list=list_db)
    Task.objects.create(name='task_2', task_list=list_db)
    Task.objects.create(name='task_3', task_list=list_db)
    list_db.save()

    br = context.browser
    br.get(context.base_url + url)


@when(u'I write a task name in the new task field for list number "{list_number}", that says: "{text}" and I click on button')
def step_impl(context, list_number, text):
    list_number = int(list_number)
    br = context.browser
    all_fields = br.find_elements_by_name("task_name")
    text_field = all_fields[list_number-1]
    text_field.send_keys(text)

    all_buttons = br.find_elements_by_class_name('btn-add-task')
    button = all_buttons[list_number-1]
    button.click()


@then(u'I should see "{text}"')
def step_impl(context, text):
    br = context.browser
    raise NotImplementedError(u'STEP: Then I should see "Buy bread and milk and beer, it\'s friday!!!"')
