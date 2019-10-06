from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import re
import json
import pymysql
from dateutil.parser import parse
from langdetect import detect
import smtplib, datetime
from email.mime.text import MIMEText

# READ:
# https://developers.google.com/youtube/v3/docs/commentThreads/list
# https://developers.google.com/youtube/v3/docs/commentThreads#resource

YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_SERVICE_NAME = "youtube"


class YouTubeComment:

    def __init__(self, data_base, channelid, developer_key_list):
        self.channelid = channelid
        self.developer_key_list = developer_key_list
        self.db = data_base.db
        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=self.developer_key_list[1])
        print('init complete')

    def _get_comment_threads(self, videoid, next_page_token):
        try:
            results = self.youtube.commentThreads().list(
                part="snippet",
                maxResults=100,
                videoId=videoid,
                textFormat="plainText",
                pageToken=next_page_token
            ).execute()
            return results
        except:
            print("error")
            return None

    def get_comments(self, videoId):

        next_page_token = ''
        further = True
        comment_count = 0
        while further:
            print(comment_count, end=' ', flush=True)
            results = self._get_comment_threads(videoId, next_page_token)
            if results is None:
                return
            next_page_token = ''

            for item in results["items"]:
                try:
                    comment_count += 1
                    comment = item["snippet"]["topLevelComment"]
                    author = re.sub('[^가-힝0-9a-zA-Z\\s]', '', comment["snippet"]["authorDisplayName"])
                    authorId = comment["snippet"]["authorChannelId"]["value"]
                    likeCount = comment["snippet"]["likeCount"]
                    publishedAt = parse(comment["snippet"]["publishedAt"], ignoretz=True)
                    text = pymysql.escape_string(comment["snippet"]["textDisplay"].replace('\n', ' '))
                    text_length = len(text)
                    text_1000 = text[:1000]
                    language = 'none'
                    if text_length >= 2:
                        try:
                            language = detect(text_1000)
                        except:
                            pass

                    self.db.execute("insert oasis.yt_comment values('%s','%s','%s','%s',%d,'%s','%s','%s',%d)" % (
                        self.channelid, videoId, author, authorId, likeCount, publishedAt, text_1000, language,
                        text_length))

                except:
                    print("ERROR ", end='')
            else:  # for-else
                try:
                    next_page_token = results["nextPageToken"]
                except KeyError as e:
                    print(videoId, "is Done, total comments =", comment_count)
                    further = False
