Feature: In order to remember my tasks, as a working person, I want to add tasks to a task list

Scenario: Add task
  Given I go to "/tasks/"
  When I write a task name in the new task field for list number "1", that says: "Buy bread and milk and beer, it's friday!!!" and I click on button
  Then I should see "Buy bread and milk and beer, it's friday!!!"

