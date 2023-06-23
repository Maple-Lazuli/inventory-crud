from dataclasses import dataclass
import psycopg2 as pg
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

from datetime import datetime, timedelta


@dataclass
class DBInteractions:
    db_name: str = 'inventory_db'
    db_user: str = 'postgres'
    db_pass: str = 'postgres'
    db_host: str = '127.0.0.1'
    db_port: str = '5432'

    def __post_init__(self):
        self.connection = pg.connect(database=self.db_name,
                                     user=self.db_user,
                                     password=self.db_pass,
                                     host=self.db_pass,
                                     port=self.db_port)

    def create_new_role(self, role_name):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"insert into roles (role_name) values (%s);", role_name)

            return True
            # Log f"Added {role_name} Successfully"

        except errors.lookup(UNIQUE_VIOLATION) as e:
            return False
            # "Unique Violation"

        except Exception as e:
            return False
            # log exception

    def get_roles(self):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"select * from roles;")

            return cur.fetchall()

        except Exception as e:
            return []
            # log exception

    def create_account(self, role_id, first_name, last_name, user_name, password, salt):

        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"""insert into accounts (role_id, first_name, last_name, created_on, username, password,
                salt) values (%(role_id)s,%(first_name)s,%(last_name)s,%(create_on)s,%(username)s,%(password)s,%(salt)s)
                ;""", {'role_id': role_id, 'first_name': first_name, 'last_name': last_name, 'username': user_name,
                       'password:': password, 'created_on': datetime.now(), 'salt': salt})

            return True
            # Log f"Added {role_name} Successfully"

        except Exception as e:
            return False

    def get_account(self, user_name):

        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"select * from accounts where username = %s;", user_name)

            return cur.fetchone()

        except Exception as e:
            return None

    def delete_account(self, user_name):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"delete * from accounts where username = %s;", user_name)

            return True

        except Exception as e:
            return False

    def update_permissions(self, role_id, user_name):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"update accounts SET role_id = %(role_id)s where username = %(user_name)s;",
                            {'role_id': role_id, 'user_name': user_name})
        except Exception as e:
            return False
            # log failure

        try:
            account_id = self.get_accounts(user_name)['account_id']

            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"""INSERT INTO permission_changes (account_id, role_id, change_date) VALUES"
                             (%(account_id)s,%(role_id)s,%(change_date)s);""",
                            {'account_id': account_id, 'role_id': role_id, 'change_date': datetime.now()})

        except Exception as e:
            return False
            # log failure

        return True

    def get_session(self, code, account_id):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"select * from sessions where session_code = %(code)s and account_id = %(account_id)s;",
                            {'code': code, 'account_id': account_id})

            return cur.fetchone()

        except Exception as e:
            return None

    def add_session(self, account_id):
        # create code
        code = "REMOVE"
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"""INSERT INTO permission_changes (account_id, creation_date, end_date, session_code, 
                active) VALUES (%(account_id)s,%(creation_date)s,%(end_date)s,%(session_code)s,%(active)s,);""",
                            {'account_id': account_id, 'creation_date': datetime.now(),
                             'end_date': datetime.now() + timedelta(hours=1),
                             'session_code': code, 'active': True})
            return code

        except Exception as e:
            return None
            # log failure

    def add_item(self, account_id, name, description, quantity):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"""INSERT INTO items (account_id, name, description, quantity, creation_date)
                 VALUES (%(account_id)s,%(name)s,%(description)s,%(quantity)s,%(creation_date)s);""",
                            {'account_id': account_id, 'name': name, 'description': description, 'quantity': quantity,
                             'creation_date': datetime.now()})

            return True

        except Exception as e:
            return None
            # log failure

    def get_items(self, item_id=None):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"select * from items where item_id = %(item_id)s;",
                            {'item_id': item_id})

            return cur.fetchone()

        except Exception as e:
            return None

    def delete_item(self, item_id):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"delete * from items where item_id = %s;", item_id)

            return True

        except Exception as e:
            return False

    def update_item(self, item_id, name, description, quantity):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"""update items SET name = %(name)s, description = %(description)s, 
                quantity = %(quantity)s, modification_date = %(modification_date)s, where item_id = %(item_id)s;""",
                            {'name': name, 'description': description, 'quantity': quantity,
                             'modification_date': datetime.now(),'item_id': item_id})
        except Exception as e:
            return False
            # log failure
