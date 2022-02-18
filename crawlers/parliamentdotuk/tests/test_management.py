from datetime import datetime
from unittest.mock import patch

import crawlers.parliamentdotuk.management.commands.bills as tasks
import crawlers.parliamentdotuk.tasks.openapi.bills.bills
from basetest.testcase import LocalManagementTestCase
from crawlers.parliamentdotuk.tasks.openapi.bills import viewmodels
from crawlers.parliamentdotuk.tasks.openapi.bills.bills import _should_update
from crawlers.parliamentdotuk.tests.openapi.data_bill import BILL_SUMMARY_DATA
from repository.models import Bill, House, ParliamentarySession
from repository.models.bill import BillType, BillTypeCategory
from repository.tests.data.create import create_sample_bill


class ManagementCommandTests(LocalManagementTestCase):
    command = "bills"

    def test_update_bills_with_id_calls_update_for_single_bill(self):
        with patch.object(
            tasks,
            "fetch_and_update_bill",
        ) as mocked_each_bill, patch.object(
            tasks, "update_bills"
        ) as mocked_all_bills, patch.object(
            tasks, "_update_type_definitions"
        ):
            self.call_command(836)
            self.assertFalse(mocked_all_bills.called)
            self.assertTrue(mocked_each_bill.called)

    def test_update_bills_without_id_calls_update_for_all_bills(self):
        with patch.object(tasks, "update_bills") as mocked_all_bills:
            self.call_command()
            self.assertTrue(mocked_all_bills.called)

    def test_update_all_bills_task_is_passed_to_taskrunner(self):
        with patch.object(
            crawlers.parliamentdotuk.tasks.openapi.bills.bills.update_bills, "delay"
        ) as mocked_all_bills:
            self.call_command(instant=False)
            self.assertTrue(mocked_all_bills.called)

    def test_should_update(self):
        summary = viewmodels.BillSummary(**BILL_SUMMARY_DATA)
        self.assertTrue(_should_update(summary))

        create_sample_bill(
            parliamentdotuk=512,
            last_update=datetime(2010, 7, 26, 16, 52, 10),
        )
        self.assertFalse(_should_update(summary))

        bill = Bill.objects.get(pk=512)
        bill.last_update = datetime(2009, 7, 26, 16, 52, 10)
        bill.save()
        self.assertTrue(_should_update(summary))

    def tearDown(self) -> None:
        self.delete_instances_of(
            Bill,
            BillType,
            BillTypeCategory,
            House,
            ParliamentarySession,
        )
