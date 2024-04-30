from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests
import re    
import os   
import json
from urllib.parse import quote

    
def get_transcript(video_id):
    try:
        results = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for result in results:
            transcript += (result['text'] + " ")
        transcript_path = os.path.join("transcript", f"id_{video_id}.txt")
        os.makedirs(os.path.dirname(transcript_path), exist_ok=True)
        with open(transcript_path, 'w') as f:
            f.write(transcript)
    except Exception as e:
        print(f"Error occurred while fetching transcript for video ID {video_id}: {e}")


def get_url_info(video_list, query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'
    }
    encoded_query = quote(query)
    r = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={encoded_query}&key=AIzaSyA_1TxT9bo6uPREpTDvQn6H2S2TGRp8JXw", headers=headers)
    
    soup = BeautifulSoup(r.text,features="html.parser")
    info_dict = soup.prettify()
    
    with open("info.txt",'w') as info:
        info.write(info_dict)
    info_dict = json.loads(info_dict)
    with open(f"video_id.txt",'a') as f:
        for item in info_dict["items"]:
            if item["id"]["videoId"] not in video_list:
                video_list.append(item["id"]["videoId"])
                f.write(item["id"]["videoId"])
                f.write("\n")
    

def main():
    with open("video_id.txt",'w') as overwrite:
        x = 1
    video_list = []
    query_list = ["lipstick recommendation","lipstick review"]
    for query in query_list:
        get_url_info(video_list, query)

    # with open("video_id.txt",'r') as f:
    #     for line in f:
    #         get_transcript(line)
            

if __name__ == "__main__":
    main()