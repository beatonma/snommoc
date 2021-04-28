from basetest.testcase import LocalTestCase
from notifications.models.task_notification import TaskNotification, task_notification


@task_notification(label='root-task')
def my_root_task(succeed, child_succeed, **kwargs):
    if succeed:
        kwargs['notification'].append('root-task succeeds')
    else:
        raise Exception('root task fails')

    my_child_task(succeed=child_succeed, **kwargs)


@task_notification(label='child-task')
def my_child_task(succeed, **kwargs):
    if succeed:
        kwargs['notification'].append('child-task succeeds')

    else:
        raise Exception('child-task fails')


class TaskNotificationTests(LocalTestCase):
    """"""

    def test_task_notification_decoration_nested_should_share_root_notification(self):
        my_root_task(succeed=True, child_succeed=True)

        self.assertQuerysetSize(TaskNotification.objects, 1)
        task = TaskNotification.objects.first()

        self.assertEqual(task.title, 'root-task')

        self.assertTrue('root-task succeeds' in task.content)
        self.assertTrue('child-task succeeds' in task.content)

        self.assertTrue(task.complete)
        self.assertFalse(task.failed)
        self.assertTrue(task.finished)


    def test_task_notification_decoration_nested_failure_should_mark_root_notification_as_failure(self):
        my_root_task(succeed=True, child_succeed=False)

        self.assertQuerysetSize(TaskNotification.objects, 1)
        task = TaskNotification.objects.first()

        self.assertEqual(task.title, 'root-task')

        self.assertTrue('root-task succeeds' in task.content)
        self.assertTrue('child-task fails' in task.content)

        self.assertFalse(task.complete)
        self.assertTrue(task.failed)
        self.assertTrue(task.finished)

    def test_task_notification_decoration_is_correct(self):
        my_child_task(succeed=True)

        self.assertQuerysetSize(TaskNotification.objects, 1)
        task = TaskNotification.objects.first()

        self.assertEqual(task.title, 'child-task')

        self.assertTrue('child-task succeeds' in task.content)

        self.assertTrue(task.complete)
        self.assertFalse(task.failed)
        self.assertTrue(task.finished)



    def tearDown(self) -> None:
        self.delete_instances_of(
            TaskNotification,
        )
