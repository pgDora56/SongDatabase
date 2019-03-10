import sqlite3, difflib

class DB:
    def __init__(self):
        self.dbpath = 'songdata.sqlite' # 本番用
        # self.dbpath = 'test.sqlite' # テスト用
        self.connection = sqlite3.connect(self.dbpath)
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + 
                                "songs (id INTEGER PRIMARY KEY, " + 
                                "title TEXT, artist TEXT, year INTEGER, type TEXT, animetitle TEXT, priority INTEGER DEFAULT 1)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + 
                                "songs_incomplete (id INTEGER PRIMARY KEY, " + 
                                "title TEXT, artist TEXT, comment TEXT, priority INTEGER DEFAULT 1)")
        except sqlite3.Error as e:
            print('sqlite3.Error occurred in DB initialize: ', e.args[0])

    def get_all(self):
        self.cursor.execute('SELECT title, artist, year, type, animetitle, priority FROM songs')
        return self.cursor.fetchall()
    
    def get_all_incomplete(self):
        self.cursor.execute('SELECT title, artist, priority FROM songs_incomplete')
        return self.cursor.fetchall()

    def get_judge(self):        
        self.cursor.execute('SELECT title, artist FROM songs')
        return self.cursor.fetchall()

    def get_judge_incomplete(self):
        self.cursor.execute('SELECT title, artist FROM songs_incomplete')
        return self.cursor.fetchall()
    
    def insert(self, data):
        # dataが5であれば (title, artist, year, type, animetitle) で取得
        # dataが3であれば (title, artist, comment) で取得
        if len(data) != 3 and len(data) != 5: return
        judge_datas = self.get_judge()
        entry = False
        for song in judge_datas:
            ratio = difflib.SequenceMatcher(None, song[0], data[0]).ratio()
            if ratio >= 0.75:
                c = ""
                if ratio == 1.0: c = "T"
                else:
                    print("☆以下の2データは同じデータですか？")
                    print("　▶ {} / {}".format(song[0], song[1]))
                    print("　▶ {} / {}".format(data[0], data[1]))
                while not c in ["T", "t", "F", "f"]:
                    c = input("T/F > ")
                if c in ["T", "t"]:
                    self.cursor.execute("UPDATE songs SET priority = priority + 1 WHERE title = ? AND artist = ?", (data[0], data[1]))
                    self.write()
                    print('{} / {} => Priority Up'.format(data[0], data[1]))
                    entry = True
                    break
        if not entry:
            judge_datas = self.get_judge_incomplete()
            for song in judge_datas:
                ratio = difflib.SequenceMatcher(None, song[0], data[0]).ratio()
                if ratio >= 0.75:
                    c = ""
                    if ratio == 1.0: c = "T"
                    else:
                        print("★以下の2データは同じデータですか？")
                        print("　▶ {} / {}".format(song[0], song[1]))
                        print("　▶ {} / {}".format(data[0], data[1]))
                    while not c in ["T", "t", "F", "f"]:
                        c = input("T/F > ")
                    if c in ["T", "t"]:
                        if len(data) == 3:
                            self.cursor.execute("SELECT comment FROM songs_incomplete WHERE title = ? AND artist = ?",(data[0], data[1]))
                            comment = self.cursor.fetchone()
                            if comment == "":
                                comment += data[2]
                            elif data[2] != "":
                                comment += "/" + data[2]
                            self.cursor.execute("UPDATE songs_incomplete SET priority = priority + 1, comment = CASE WHEN comment == '' THEN ? ELSE comment||? WHERE title = ? AND artist = ?", (data[2], data[2], data[0], data[1]))
                        elif len(data) == 5:                            
                            self.cursor.execute("SELECT priority FROM songs_incomplete WHERE title = ? AND artist = ?", (data[0], data[1]))
                            priority = self.cursor.fetchone() + 1
                            self.cursor.execute("INSERT INTO songs(title, artist, year, type, animetitle, priority) VALUES(?, ?, ?, ?, ?, ?)", data + (priority))
                            self.cursor.execute("DELETE FROM songs_incomplete WHERE title = ? AND artist = ?", (data[0], data[1]))
                        self.write()
                        print('{} / {} => Priority Up'.format(data[0], data[1]))
                        entry = True
                        break
        if not entry:
            if len(data) == 3: 
                self.cursor.execute("INSERT INTO songs_incomplete(title, artist, comment) VALUES(?, ?, ?)", data)
                print('{} / {} => Add to incomplete'.format(data[0], data[1]))
            elif len(data) == 5: 
                self.cursor.execute("INSERT INTO songs(title, artist, year, type, animetitle) VALUES(?, ?, ?, ?, ?)", data)
                print('{} / {} => Add'.format(data[0], data[1]))
            self.write()

    def write(self):
        self.connection.commit()

    def wq(self):
        self.connection.commit()
        self.connection.close()
