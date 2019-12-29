import csv
import re
from lw.core.models import User


class UsersImporter():

    def __init__(self, csv_path):
        self.csv_path = csv_path


    def run(self):
        with open(self.csv_path) as f:
            users = csv.DictReader(f, delimiter=',')
            self.bulk_import(users)


    def bulk_import(self, users):
        for user_params in users:
            user = self.build_user(user_params)
            user.save()


    def build_user(self, user_params):
        new_password_hash = self.prepare_password(user_params['pass'])
        user = User(
                password=new_password_hash,
                username=user_params['name'],
                email=user_params['mail'])

        return user


    def prepare_password(self, old_password_hash):
        new_password_hash = re.sub(r'^\$S', 'drupal_sha512', old_password_hash)
        return new_password_hash
