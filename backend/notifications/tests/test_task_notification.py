from basetest.testcase import LocalTestCase
from notifications.models.task_notification import TaskNotification, task_notification


class _ParentException(Exception):
    pass


class _ChildException(Exception):
    pass


@task_notification(label="root-task")
def my_root_task(succeed, child_succeed, **kwargs):
    if succeed:
        kwargs["notification"].append("root-task succeeds")
    else:
        raise _ParentException("root task fails")

    my_child_task(succeed=child_succeed, **kwargs)


@task_notification(label="child-task")
def my_child_task(succeed, **kwargs):
    if succeed:
        kwargs["notification"].append("child-task succeeds")

    else:
        raise _ChildException("child-task fails")


class TaskNotificationDecorationTests(LocalTestCase):
    def test_nested_should_share_root_notification(self):
        """Nested tasks should share the same TaskNotification instance."""
        my_root_task(succeed=True, child_succeed=True)

        self.assertQuerysetSize(TaskNotification.objects, 1)
        task = TaskNotification.objects.first()

        self.assertEqual(task.title, "root-task")

        self.assertTrue("root-task succeeds" in task.content)
        self.assertTrue("child-task succeeds" in task.content)

        self.assertTrue(task.complete)
        self.assertFalse(task.failed)
        self.assertTrue(task.finished)

    def test_nested_failure_should_mark_root_notification_as_failure(self):
        """If nested child task fails, parent notification should be marked as failure."""
        with self.assertRaises(_ChildException):
            my_root_task(succeed=True, child_succeed=False)

        self.assertQuerysetSize(TaskNotification.objects, 1)
        task = TaskNotification.objects.first()

        self.assertEqual(task.title, "root-task")

        self.assertTrue("root-task succeeds" in task.content)
        self.assertTrue("child-task fails" in task.content)

        self.assertFalse(task.complete)
        self.assertTrue(task.failed)
        self.assertTrue(task.finished)

    def test_task_notification_decoration_is_correct(self):
        my_child_task(succeed=True)

        self.assertQuerysetSize(TaskNotification.objects, 1)
        task = TaskNotification.objects.first()

        self.assertEqual(task.title, "child-task")

        self.assertTrue("child-task succeeds" in task.content)

        self.assertTrue(task.complete)
        self.assertFalse(task.failed)
        self.assertTrue(task.finished)

    def tearDown(self) -> None:
        self.delete_instances_of(
            TaskNotification,
        )
