from behave import given, when, then


@given(u'I go to "{url}"')
def step_impl(context, url):
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
    assert text in br.page_source
