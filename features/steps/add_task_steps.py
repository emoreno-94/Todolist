from behave import *

@given(u'I go to "/tasks"')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + "/tasks")


@when(u'I fill in field with id "new_task" with "Buy bread and milk and beer, it\'s friday!!!" and I click on "add_task"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I fill in field with id "new_task" with "Buy bread and milk and beer, it\'s friday!!!" and I click on "add_task"')


@then(u'I should see "Buy bread and milk and beer, it\'s friday!!!"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should see "Buy bread and milk and beer, it\'s friday!!!"')
