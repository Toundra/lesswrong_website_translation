from django.test import TestCase
from lw.core.models import User
from .users_importer import UsersImporter


class UsersImporterTest(TestCase):

    def test_import_users(self):
        # TODO relative path
        csv_path = '/code/services/data_migrations/importers/users/fixtures/users.csv'
        old_count = User.objects.count()

        UsersImporter(csv_path).run()

        count = User.objects.count()
        self.assertEqual(old_count + 1, count)
