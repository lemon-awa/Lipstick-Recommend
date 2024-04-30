import get_product_detail
import json

def main():
    db = None
    # Get data from json file
    with open("database1355.json") as f:
        db = json.load(f)
    database = {}

    # Get Sephora info, restructure data
    for product_url, video_info in db.items():
        product_info = {}
        product_info["mentioned"] = video_info
        product_info["source"] = product_url
        sephora_info = get_product_detail.get_product_detail(product_url)
        product_info.update(sephora_info)
        database[product_url] = product_info
        
    # Export updated data
    with open('database1355_sephota.json', 'w') as f:
        json.dump(database, f)
    

main()