import googleapiclient.discovery
import pandas as pd
import socket
import s3fs

api_service_name = 'youtube'
api_version = 'v3'
DEVELOPER_KEY = 'AIzaSyCML2-dJFqBviYGdSSAbJ8WLsAsnFKxaBZdI'
videoId = 'M__WZPd2r58'

class YoutubeScrapper:
  def __init__(self, api_service_name, api_version, DEVELOPER_KEY, videoId):
    try:
      "first function will run"
      print('Scrapping youtube data started...')
      
      # 1. konfigurasi api
      self.videoId = videoId
      self.youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
      self.df = None
      
      self.get_comments()
      self.download_csv()
    except socket.timeout:
      print('Error: Connection to Youtube API (Timeout). Check your internet')
    except Exception as e:
      print(f'Error Unexpected {e}')
      
  def get_comments(self):
    request = self.youtube.commentThreads().list(
      part = 'snippet',
      videoId = self.videoId,
      maxResults =1000
    )

    # mengeksekusi respons
    response = request.execute()

    comments = []

    for item in response['items']:
      comment = item['snippet']['topLevelComment']['snippet']
      comments.append([
        comment['authorDisplayName'],
        comment['publishedAt'],
        comment['updatedAt'],
        comment['likeCount'],
        comment['textDisplay']
      ])
      
    self.df = pd.DataFrame(comments, columns = ['author', 'published_at', 'updated_at', 'like_count', 'text'])
  
  def download_csv(self):
    # download file
    file_name = f's3://steven-airflow-youtube-bucket/{self.videoId}.csv'
    self.df.to_csv(file_name, index = False, encoding='utf-8')
    print(f'File {file_name} has been downloaded')

def run_pipeline():
  YoutubeScrapper(api_service_name, api_version, DEVELOPER_KEY, videoId)