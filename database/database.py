import pymysql


class DataBase:

    def __init__(self):
        connect = pymysql.connect(host='localhost', user='root', password='1qazxc', db='oasis', charset='utf8mb4',
                                  autocommit=True, port=3306)
        db = connect.cursor()
        self.db = db

    def db_reconnect(self):
        connect = pymysql.connect(host='localhost', user='root', password='1qazxc', db='oasis', charset='utf8mb4',
                                  autocommit=True, port=3306)
        db = connect.cursor()
        self.db = db

    def get_video_list(self, channelid):
        SQL = "SELECT videoId, videoTitle FROM oasis.yt_videoid WHERE channelId= '%s'"
        self.db.execute(SQL % channelid)
        video_list = self.db.fetchall()
        return video_list
