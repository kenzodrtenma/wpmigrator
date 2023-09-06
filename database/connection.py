from database.environment import ORIGIN_DB, DESTINY_DB, PREFIXES
import mysql.connector
from mysql.connector import errorcode
from utils.bcolors import bcolors

class Connection:
    def __init__(self, environment='origin'):
        self._environments = {
            'origin': ORIGIN_DB,
            'destiny': DESTINY_DB
        }
        self._env_prefix = PREFIXES[environment]
        self._env_conn_object = self._environments[environment]
        self._cnx = mysql.connector.connect(**self._env_conn_object)
        self._cursor = self._cnx.cursor()


    def queryBy(self, params, table, limit=0, relation='AND'):
        if limit:
            limit = " LIMIT {}".format(limit)
        else:
            limit = ""

        count = 1
        whereClause = ""
        for key in params.keys():
            if count == 1:
                clause = 'WHERE'
            else:
                clause = ' {}'.format(relation)
            
            whereClause = whereClause + "{} {} = %({})s".format(clause, key, key)
            count += 1

        query = "SELECT * FROM {} {}{}".format(
            self._setTableName(table),
            whereClause,
            limit
        )

        self._cursor.execute(query, params)
        result = self._cursor.fetchall()
        self._close()

        return result
    
    def insert(self, table, params):
        keys = ", ".join(params.keys())
        values = []
        counter = 1
        while counter <= len(params.keys()):
            values.append('%s')
            counter+=1     
        values = ", ".join(values)

        query = "INSERT INTO {} ({}) VALUES ({})".format(self._setTableName(table), keys, values)

        self._cursor.execute(query, list(params.values()))
        rowid = self._cursor.lastrowid
        self._cnx.commit()
        self._close()
        return rowid

    def handleException(err):
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(bcolors.FAIL + 'Usuário ou senha de acesso ao banco de dados está incorreto.\n\n' + bcolors.ENDC)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(bcolors.FAIL + "O banco de dados fornecido não existe.\n\n" + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "Ocorreu um erro de banco de dados. (Detalhe: {})\n\n".format(err) + bcolors.ENDC)

    def _setTableName(self, table):
        return "{}{}".format(self._env_prefix, table)
    
    def _close (self):
        print(bcolors.OKBLUE + "  {}".format(self._cursor.statement) + bcolors.ENDC)
        self._cursor.close()
        self._cnx.close()