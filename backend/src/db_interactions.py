from dataclasses import dataclass
import psycopg2 as pg
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
import random

from datetime import datetime, timedelta
import hashlib


def generate_code():
    hasher = hashlib.sha512()
    hasher.update(f"{datetime.now()} {random.randint(1, 100000)}".encode())
    return hasher.hexdigest()


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
                                     host=self.db_host,
                                     port=self.db_port)

    def create_new_role(self, role_name):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute("insert into roles (role_name) values (%(r)s);", {'r': role_name})

            return True
            # TODO
            # Log f"Added {role_name} Successfully"

        except errors.lookup(UNIQUE_VIOLATION) as e:
            print(e)
            return False
            # TODO
            # "Unique Violation"

        except Exception as e:
            print(e)

            return False
            # TODO
            # log exception

    def get_roles(self):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"select * from roles;")
                return cur.fetchall()

        except Exception as e:
            print(e)
            return []
            # TODO
            # log exception

    def create_account(self, role_id, first_name, last_name, user_name, password, salt):

        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"""insert into accounts (role_id, first_name, last_name, created_on, username, password,
                    salt) values (%(role_id)s,%(first_name)s,%(last_name)s,%(created_on)s,%(username)s,
                    %(password)s,%(salt)s);""", {'role_id': 1, 'first_name': first_name, 'last_name':
                    last_name, 'username': user_name, 'password': password, 'created_on': datetime.now(), 'salt': salt})

            return True
            # TODO
            # Log f"Added {role_name} Successfully"

        except Exception as e:
            print(e)
            return False
        # TODO

    def get_account(self, user_name=None, account_id=None):

        try:
            if user_name is not None:
                with self.connection, self.connection.cursor() as cur:
                    cur.execute(f"select * from accounts where username = %(u)s;", {'u': user_name})
                    return cur.fetchone()

            elif account_id is not None:
                with self.connection, self.connection.cursor() as cur:
                    cur.execute(f"select * from accounts where account_id = %(id)s;", {'id': account_id})

                    return cur.fetchone()

        except Exception as e:
            print(e)
            return None
        # TODO

    def delete_account(self, user_name):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"delete from accounts where username = %(u)s;", {'u': user_name})

            return True

        except Exception as e:
            print(e)
            return False
        # TODO

    def update_permissions(self, role_id, account_id):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"update accounts SET role_id = %(role_id)s where account_id = %(account_id)s;",
                            {'role_id': role_id, 'account_id': account_id})
        except Exception as e:
            print(e)
            return False
            # log failure
        # TODO

        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"""INSERT INTO permission_changes (account_id, role_id, change_date) VALUES
                             (%(account_id)s,%(role_id)s,%(change_date)s);""",
                            {'account_id': account_id, 'role_id': role_id, 'change_date': datetime.now()})

        except Exception as e:
            print(e)
            return False
            # log failure
        # TODO

        return True

    def get_permission_changes(self):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"select * from permission_changes;")
                return cur.fetchall()

        except Exception as e:
            print(e)
            return []
            # TODO
            # log exception

    def get_session(self, code, account_id):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"select * from sessions where session_code = %(code)s and account_id = %(account_id)s;",
                            {'code': code, 'account_id': account_id})

                return cur.fetchone()

        except Exception as e:
            print(e)
            return None
        # TODO

    def add_session(self, account_id):
        # create code
        code = generate_code()
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"""INSERT INTO sessions (account_id, creation_date, end_date, session_code) VALUES
                 (%(account_id)s,%(creation_date)s,%(end_date)s,%(session_code)s);""",
                            {'account_id': account_id, 'creation_date': datetime.now(),
                             'end_date': datetime.now() + timedelta(hours=10),
                             'session_code': code})
            return code

        except Exception as e:
            print(e)
            return None
            # log failure
        # TODO

    def add_item(self, account_id, name, description, quantity):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"""INSERT INTO items (account_id, name, description, quantity, creation_date)
                 VALUES (%(account_id)s,%(name)s,%(description)s,%(quantity)s,%(creation_date)s);""",
                            {'account_id': account_id, 'name': name, 'description': description, 'quantity': quantity,
                             'creation_date': datetime.now()})

            return True

        except Exception as e:
            print(e)
            return None
            # log failure
        # TODO

    def get_items(self, item_id=None):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"select * from items where item_id = %(item_id)s;",
                            {'item_id': item_id})

                return cur.fetchone()

        except Exception as e:
            print(e)
            return None
        # TODO

    def delete_item(self, item_id):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"delete * from items where item_id = %s;", item_id)

            return True

        except Exception as e:
            print(e)
            return False
        # TODO

    def update_item(self, item_id, name, description, quantity):
        try:
            with self.connection, self.connection.cursor() as cur:
                cur.execute(f"""update items SET name = %(name)s, description = %(description)s, 
                quantity = %(quantity)s, modification_date = %(modification_date)s, where item_id = %(item_id)s;""",
                            {'name': name, 'description': description, 'quantity': quantity,
                             'modification_date': datetime.now(), 'item_id': item_id})
        except Exception as e:
            print(e)
            return False
            # log failure
        # TODO


if __name__ == "__main__":
    interactor = DBInteractions()

    # Roles
    print("ROLES")
    print(interactor.get_roles())
    print(interactor.create_new_role("Administrator"))
    print(interactor.create_new_role("Manager"))

    print(interactor.get_roles())

    # Accounts
    print("ACCOUNTS")
    roles = interactor.get_roles()[0]
    id = roles[0]
    print(interactor.create_account(id, "Ada", "Lazi", "adalazi", 'aasd', 111))
    print(interactor.create_account(id, "Jess", "Chavi", "jesschavi", 'aasd', 111))
    print(interactor.get_account(user_name="adalazuli"))
    print(interactor.get_account(account_id=2))
    print('delete')
    print(interactor.delete_account("jesschavi"))
    print(interactor.get_account("jesschavi"))

    # permissions
    print("PERMISSION CHANGES")
    roles = interactor.get_roles()[1]
    id = roles[0]
    print(interactor.get_permission_changes())
    print(interactor.update_permissions(role_id=id, account_id=1))
    print(interactor.get_permission_changes())
    print(interactor.get_account(account_id=1))

    # sessions
    print("SESSIONS")
    roles = interactor.get_account(user_name="adalazi")
    id = roles[0]
    code = interactor.add_session(id)
    print(f"Created code: {code}")
    print(interactor.get_session(code=code, account_id=id))



