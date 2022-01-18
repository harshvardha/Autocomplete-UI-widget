import sqlite3
conn = sqlite3.connect("dictionaryDatabase.db")
#conn.execute("CREATE TABLE nameDictionary(rank INTEGER NOT NULL,use_count INTEGER NOT NULL,word TEXT NOT NULL);")
#conn.execute("CREATE TABLE diseaseDictionary(rank INTEGER NOT NULL,use_count INTEGER NOT NULL,word TEXT NOT NULL);")
#conn.execute("CREATE TABLE symptomsDictionary(rank INTEGER NOT NULL,use_count INTEGER NOT NULL,word TEXT NOT NULL);")
#conn.execute("CREATE TABLE medicineDictionary(rank INTEGER NOT NULL,use_count INTEGER NOT NULL,word TEXT NOT NULL);")
#conn.execute("CREATE TABLE pathologicalInfoDictionary(rank INTEGER NOT NULL,use_count INTEGER NOT NULL,word TEXT NOT NULL);")

conn.execute("INSERT INTO pathologicalInfoDictionary(rank,use_count,word) VALUES(1,1,'have');")
conn.execute("INSERT INTO pathologicalInfoDictionary(rank,use_count,word) VALUES(1,1,'an');")
conn.execute("INSERT INTO pathologicalInfoDictionary(rank,use_count,word) VALUES(1,1,'x-ray');")
conn.commit()
print(conn.execute("SELECT * FROM pathologicalInfoDictionary;").fetchall())
conn.close()