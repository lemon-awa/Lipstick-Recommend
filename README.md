# Lipstick Expert

## Create environment
```bash
pip install -r requirements.txt
```


# Create Database
## Get all video_id
```bash
python get_video_id.py
```
You can change `query_list` in the main of `get_video_id.py` to get different video_id. And we get `video_id.txt`.


## Get video infomation
### please download the dataset used for sentiment analysis training at first.
```bash
tar -xvzf posdata.tar.gz
rm -rf posdata.tar.gz
tar -xvzf negdata.tar.gz
rm -rf negdata.tar.gz
```

### How to get video infomation
Please name all your video_id data with the format like  `video_{num}.txt`. One video_id dataset should contain no more than **100** video_id to avoid data loss. Result data for each dataset would be restored in `data_{num}.json`.
You can run `get_video_info.py` like this:
```bash
python get_video_info.py num
```
After you get all `.json`, you can merge all these json files by comment the parts in "__main__" that are not commented, and uncomment the parts that are commented, and then run:
```bash
python get_video_info.py
```

### Database
After the first phrase of data collection, you could get database named `video_info_database.json`.

## Get product information
First of all, we store the all color information we collected before in `color.json`, you should guarantee that `color.json` in the same folder of `get_db.py`. Besides, you need the database you get from the last step, if you database named `video_info_database.json`, you can just run the code like.
```bash
python get_db.py video_info_database.json
```
### Database
After running this python file, you could get database with both video and product information named `database_with_sephora.json`

## Train and calculate score
After we get the final json file, we rename it as final.json with sephora data inside, we run:
```bash
python scoring.py
```
The function will read in the json file and otuput a processed json file "score_list.json" with scoring infomation inside which is needed by UI part.
