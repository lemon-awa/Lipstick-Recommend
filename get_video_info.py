from bs4 import BeautifulSoup
from typing import List
import requests
import re
import json
import sys
from itertools import islice
from youtube_comment_downloader import *
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from naivebayes import sentimental_train, prepare, predictNaiveBayes
import time

def get_info(soup,type,id):
    """
    Get likes/views/subcribers information using regular expression.
    """
    try:
        if type == "subcribers":
            pattern = re.compile(r'"(\d+.\d*[A-Za-z]*) subscribers"')
        elif type == "likes":
            pattern = re.compile(r'"accessibilityText":"(\d+(?:\.\d+)?(?:\s*\w*)) likes"')
        elif type == "views":
            pattern = re.compile(r'"shortViewCount":{"simpleText":"(\d+\.?\d*[A-Za-z]*) views"')
        elif type == "time":
            pattern = re.compile(r'"dateText":{"simpleText":"(\w+ \d{1,2}, \d{4})"')
        elif type == "duration":
            pattern = re.compile(r'"approxDurationMs":"(\d+)"')
        texts = soup.find_all(string=pattern)

        info = []
        for text in texts:
            match = pattern.search(text)
            if match:
                info.append(match.group(1))
        count = info[0]
        return count
    except Exception as e:
        print(f"Error occurred while fetching transcript for video ID {id} and {type}: {e}")


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

def process_data(data):
    """
    Transfer all likes/views/subcribers data into int.
    """
    if not data:
        return None
    data = data.replace(' ', '')
    if data[-1].lower() == 'k':
        return int(float(data[:-1]) * 1000)
    elif data[-1].lower() == 'm':
        return int(float(data[:-1]) * 1000000)
    elif data[-1].lower() == 'n':
        return int(float(data[:-7]) * 1000000)
    else:
        return int(data)

def get_shortdescription(soup):
    """
    Get description of all video.
    """
    script_tag = soup.find("script", string=re.compile(r"shortDescription"))
    if script_tag:
        script_content = script_tag.string
        match = re.search(r"var ytInitialPlayerResponse = ({.*?});", script_content, re.DOTALL)
        if match:
            json_data = json.loads(match.group(1))
            short_description = json_data.get("videoDetails", {}).get("shortDescription", "")
            # print(short_description)
    return short_description

def find_products(short_description: str):
    """
    Extract all products mentioned in the description.
    """
    product_list = []
    recording = False
    lines = short_description.split("\n")
    record_signals = ["PRODUCT", "P R O D U C T", 'L I P S T I C K', "links", "MENTION", "Products"]
    junk_signals = [
        "US",
        "global",
        "com",
        "wear",
        "thank",
        "me",
        "favorite",
        "email",
        "my",
        "best",
        "place",
        "mention",
        "skin",
        "instagram",
        "twitter",
        "facebook",
        "pinterest",
        "tiktok",
        "tik tok",
        "youtube",
        "snapchat",
        "social media",
        "follow",
        "subscribe",
        "like",
        "comment",
        "share",
        "discount",
        "code",
        "coupon",
        "promo",
        "sale",
        "offer",
        "deal",
        "shop",
        "store",
        "website",
        "channel",
        "profile",
        "account",
        "off",
        "sponse",
        "sponsor",
        "sephora",
        "ulta",
        "nordstrom",
        "macys",
        "macy's",
        "amazon",
        "Video",
        "playlist",
        "Background music",
        "Disclaimer",
        "subscribe",
        "thank you for watching",
        "creators",
        "links",
        "link",
        "NEW UPLOADS",
        "Video editor",
        "Autumn Makeup video",
        "Tinted Balm video",
        "Look w/",
        "Shirt",
        "Dress",
        "Top",
        "Earrings",
        "Hair clip",
        "MAKEUP TIP",
        "HOW TO",
        "Related Video",
        "Popular Videos",
        "Available in",
        "Sweater",
        "WATCH",
        "STEP BY STEP",
        "PLAYLIST",
        "OVERHEAD",
        "Sunscreen",
        "Cleansing Balm",
        "Lash Lift",
        "Kay Beauty",
        "Hair tools",
        "Hair growth serum",
        "Collagen powder",
        "Beauty sponge",
        "Multi-purpose balm",
        "Milani",
        "Makeup by Mario",
        "L'oreal Paris",
        "Kosas",
        "Patrick Ta",
        "Haleys Beauty",
        "Sweed Lashes",
        "Simply Nam",
        "intro",
        "outro",
        "history",
        "description"
    ]

    for i, line in enumerate(lines):
        line = lines[i].strip()
        if not recording and any(record_signal.lower() in line.lower() for record_signal in record_signals):
            if len(line.split()) < 10:
                # print(line)
                recording = True
                continue
        # if "PRODUCT" in line or "LIPSTICK" in line or "P R O D U C T" in line or 'L I P S T I C K' in line or "links" in line.lower():
        #     if len(line.split()) < 10:
        #         recording = True
        #         continue
        if recording and line == "" and i + 1 < len(lines) and lines[i + 1].strip() == "":
            break
        # print(str(recording) + line)
        if recording and line != "" :
            if 'http' in line:
                line = line.split('http')[0].strip()
            if line:
                if len(line) < 5 or len(line.split()) == 1 or any(junk_signal.lower() in line.lower() for junk_signal in junk_signals):
                    continue
                if len(line.split()) < 20 and line not in product_list:
                    product_list.append(line)
                else:
                    break
    
    return product_list

def get_num_pos(comments, class_probs, word_cond_probs, vocab_size, pos_sum, neg_sum):
    """
    Calculate the ratio of postive comments.
    """
    if len(comments) == 0:
        return 0
    count = 0
    for comment in comments:
        stemmed_tokens = prepare(comment)
        emotion = predictNaiveBayes(stemmed_tokens, class_probs, word_cond_probs, vocab_size, pos_sum, neg_sum)
        if emotion == "pos":
            count += 1
    
    return count/len(comments)



def get_score_list(video_id: str, class_probs, word_cond_probs, vocab_size, pos_sum, neg_sum):
    """
    Get all information needed to score the products.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    # with open(f"soup_{video_id}.txt",'w') as f:
    #     f.write(str(soup.prettify()))
    top_10_comments = []
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)
    for comment in islice(comments, 10):
        top_10_comments.append(comment['text'])
    num_pos = get_num_pos(top_10_comments, class_probs, word_cond_probs, vocab_size, pos_sum, neg_sum)
    try:
        subscribers = get_info(soup, "subcribers", video_id)
        subscribers = process_data(subscribers)
        likes = get_info(soup, "likes", video_id)
        likes = process_data(likes)
        views = get_info(soup, "views", video_id)
        views = process_data(views)
        # time = get_info(soup, "time", video_id)
        # duration = get_info(soup, "duration", video_id)
        score_dict = {
            'Video_id': video_id,
            'Subscribers': subscribers,
            'Likes': likes,
            'Views': views,
            # 'Time': time,
            # 'Duration': duration
            "num_pos": num_pos,
        }
    except RuntimeError as e:
            print(e)
    try:
        short_description = get_shortdescription(soup)
        product_list = find_products(short_description)
    except RuntimeError as e:
            print(e)
    # print(score_dict)
    # print(product_list)
    return score_dict, product_list


def find_sephora(product_list: List[str], video_id):
    """
    Using product name to find its url using Sephora.
    """
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    first_product_links = []
    try:
        driver.get("https://www.sephora.com")
        time.sleep(5)

        for search_query in product_list:
            search_box = driver.find_element(By.NAME, "keyword")
            search_box.clear()
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(5) 
            try:
                first_product_link = driver.find_element(By.CSS_SELECTOR, ".css-klx76").get_attribute('href')
                if "lip" in first_product_link and first_product_link not in first_product_links:
                    first_product_links.append(first_product_link)
                    # print(first_product_link)
            except WebDriverException as e:
                print(f"WebDriverException: {e} and {video_id}")
            except:
                print(f"Search Query: {search_query}, First Product Link: Not found")

            driver.get("https://www.sephora.com")
            time.sleep(5) 

    finally:
        driver.quit()
        return first_product_links


def get_info_list(video_ids:List[str], database, class_probs, word_cond_probs, vocab_size, pos_sum, neg_sum):
    """
    Get all video info.
    """
    for video_id in video_ids:
        score_dict, product_list = get_score_list(video_id, class_probs, word_cond_probs, vocab_size, pos_sum, neg_sum)
        if product_list:
            first_product_links = find_sephora(product_list,video_id)
            for link in first_product_links:
                if link not in database:
                    database[link] = [score_dict]
                else:
                    database[link].append(score_dict)
    return database

def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{file_path}': {e}")
        return None

def merge_dictionaries(dict_list):
    merged_dict = {}
    for d in dict_list:
        for key, value in d.items():
            if key in merged_dict:
                merged_dict[key].extend(value)
            else:
                merged_dict[key] = value
    return merged_dict

def run_main(file_name, num, class_probs, word_cond_probs, vocab_size, pos_sum, neg_sum):
    with open(file_name, "r") as f:
        video_ids = [line.strip() for line in f]
    database ={}    
    database = get_info_list(video_ids, database,  class_probs, word_cond_probs, vocab_size, pos_sum, neg_sum)
    with open(f'data_{num}.json', 'w') as f:
        json.dump(database, f)


if __name__ == "__main__":
    class_probs,word_cond_probs,vocab_size,pos_sum,neg_sum = sentimental_train()
    num = sys.argv[1]
    file = f"video_id_{num}.txt"
    run_main(file, num , class_probs, word_cond_probs, vocab_size, pos_sum, neg_sum)

    # # merge files
    # file_paths = ["database1200.json", "database1201-1355.json"]
    # dict_list = [read_json(file_path) for file_path in file_paths]
    # merged_dict = merge_dictionaries(dict_list)
    # with open(f'database1355.json', 'w') as f:
    #     json.dump(merged_dict, f)
