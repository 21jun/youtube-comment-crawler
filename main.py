from database.database import DataBase
from youtube.YouTubeAPI import YouTubeComment
import numpy as np

# https://tools.digitalmethods.net/netvizz/youtube/mod_videos_list.php

DEVELOPER_KEY_LIST = []

def load_keys(path='APIKEYLIST.txt'):
    with open(path) as f:
        keys = f.readlines()
    content = [key.strip() for key in keys] 
    global DEVELOPER_KEY_LIST 
    DEVELOPER_KEY_LIST = content


def routine(channelid):
    db = DataBase()
    video_list = db.get_video_list(channelid)
    video_list = np.array(video_list)
    # video_list[:, 0]
    yt = YouTubeComment(db, channelid, DEVELOPER_KEY_LIST)

    for videoid in video_list[:, 0]:
        print(videoid, end='|', flush=True)
        yt.get_comments(videoid)


if __name__ == "__main__":
    load_keys()
    print(DEVELOPER_KEY_LIST)
    routine('UCsvn_Po0SmunchJYOWpOxMg')

