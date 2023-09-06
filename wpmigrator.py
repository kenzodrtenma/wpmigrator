from tables.user import User
from database.connection import Connection
import mysql.connector

from utils.bcolors import bcolors

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
                print(bcolors.FAIL + '\n\n{}\n\n'.format(err) + bcolors.ENDC)

            else:
                print(bcolors.OKGREEN + '\n\nMigração concluída com sucesso. :)\n\n' + bcolors.ENDC)
                exit_signal = True



App().run()