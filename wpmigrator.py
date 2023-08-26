from tables.user import User
from database.connection import Connection
import mysql.connector

class App:
    def __init__(self):
        self.tables = {
            'users': User
        }

        self.table = 'users'
    
    def run(self):
        exit_signal = False
        while not exit_signal:
            try:
                self.tables[self.table]().run()
            
            except mysql.connector.Error as err:
                Connection.handleException(err)
            
            except Exception as err:
                print('\n\n{}\n\n'.format(err))

            else:
                print('\n\nMigração concluída com sucesso. :)\n\n')
                exit_signal = True



App().run()