import sqlite3
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class databaseManager:
    def __init__(self,username,password,Type):
        self.username = username
        self.password = password
        self.Type = Type
        self.selectQuery = "SELECT * FROM "+self.Type+";"
        self.insertQuery = "INSERT INTO "+self.Type+"(rank,use_count,word) VALUES (?,?,?);"
        self.updateQuery = "UPDATE "+self.Type+" SET rank = '%d',use_count = '%d' WHERE word = '%s';"
        self.connection = None
        self.db_path = os.path.join(BASE_DIR,"dictionaryDatabase.db")

    def createConnection(self):
        print("request arrived")
        if(self.username=="december2019" and self.password=="31/12/19"):
            print("request arrived")
            self.connection = sqlite3.connect(self.db_path)

    def executeQuery(self,queryType,queryArguments = None):
        if(queryType=="SELECT" and queryArguments==None):
            cursor = self.connection.execute(self.selectQuery)
            return cursor.fetchall()
        elif(queryType=="INSERT"):
            self.connection.execute(self.insertQuery,queryArguments)
        elif(queryType=="UPDATE"):
            self.connection.execute(self.updateQuery%queryArguments)

    def closeConnection(self):
        self.connection.close()
