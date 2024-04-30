# import requests
import json
from math import log2, log10
import numpy as np
from collections import defaultdict
from itertools import islice


def scoring(score_info, subscriber_param, likes_param, views_param, pos_param):
    """Calculate the score of a video based on its subsribers, likes, views, and positive ratio"""
    final_score = {}
    for product, infos in score_info.items():
        scores = []
        mention_list = infos["mentioned"]
        for mention_data in mention_list:
            if mention_data["Subscribers"] is None:
                mention_data["Subscribers"] = 1
            if mention_data["Likes"] is None:
                mention_data["Likes"] = 1
            if mention_data["Views"] is None:
                mention_data["Views"] = 1
            if mention_data["num_pos"] is None:
                mention_data["num_pos"] = 0
            score = (subscriber_param * max(log10(mention_data["Subscribers"]), 1) + 
                     likes_param * max(log10(mention_data["Likes"]), 1) + 
                     views_param * max(log10(mention_data["Views"]), 1) + 
                     pos_param * 10 * mention_data["num_pos"])
            scores.append(score)
            score_info[product]["score"] = score
        scores = sorted(scores, reverse=True)
        final_value = 0
        for i, value in enumerate(scores):
            if i != 0:
                final_value += value / log2(i+1)
            else:
                final_value += value
        final_score[product] = final_value
    return final_score, score_info

def calculate_distance(calculated_rank, product_rank_dict):
    """Calculate the kendall-tau distance between calculated rank and product rank"""
    X = 0
    Y = 0
    for i in range(len(calculated_rank)):
        for j in range(i+1, len(calculated_rank)):
            if product_rank_dict[calculated_rank[i]] < product_rank_dict[calculated_rank[j]]:
                X += 1
            else:
                Y += 1
    # print(X, Y)
    return (X - Y) / (X + Y)

def train(score_info, product_rank_dict):
    """Tune the parameter based on the kendall-tau distance"""
    max_d = 0
    best_sub = 0
    best_like = 0
    best_view = 0
    best_pos = 0
    for subscriber_param in np.arange(0.01, 1.01, 0.01):
        print(subscriber_param) # treat as progress bar
        for likes_param in np.arange(0.01, 1.01 - subscriber_param, 0.01):
            for views_param in np.arange(0.01, 1.01 - subscriber_param - likes_param, 0.01):
                pos_param = 1 - subscriber_param - likes_param - views_param
                if pos_param < 0:
                    continue
                # print(subscriber_param, likes_param, views_param, pos_param)
                final_score, score_info = scoring(score_info,subscriber_param,likes_param,views_param,pos_param)
                # print(final_score)
                calculated_rank = sorted(final_score, key = final_score.get, reverse= True)
                # print(calculated_rank)
                d = calculate_distance(calculated_rank, product_rank_dict)
                if d > max_d:
                    best_sub = subscriber_param
                    best_like = likes_param
                    best_view = views_param
                    best_pos = pos_param
                    max_d = d
                    # print(best_sub, best_like, best_view, best_pos, max_d)
                    # print(final_score)
                    # print(calculated_rank)
                    # print(product_rank_dict)
    return best_sub, best_like, best_view, best_pos

def get_final_rank(score_info, product_rank_dict, best_sub, best_like, best_view, best_pos):
    """Get the final rank of the product"""
    final_score, score_info = scoring(score_info, best_sub, best_like, best_view, best_pos)
    calculated_rank = sorted(final_score, key = final_score.get, reverse= True)
    d = calculate_distance(calculated_rank, product_rank_dict)
    return d, calculated_rank, score_info

def evaluate(product_info, best_sub, best_like, best_view, best_pos):
    """Evaluate the model based on the different size of data"""
    data_10 = dict(islice(product_info.items(), 10))
    data_30 = dict(islice(product_info.items(), 30))
    data_50 = dict(islice(product_info.items(), 50))
    data_100 = dict(islice(product_info.items(), 100))
    data_200 = dict(islice(product_info.items(), 200))
    datas = [data_10, data_30, data_50, data_100, data_200]
    
    for data in datas:
        product_sales_info = []
        product_rank_dict = {}
        for key, value in data.items():
            # print(key, value)
            product_sales_info.append([key, (value['love'] * value['star']/5)])
        sorted_product_rank = sorted(product_sales_info, key=lambda x: x[1], reverse=True)
        i = 0
        for item in sorted_product_rank:
            product_rank_dict[item[0]] = i
            i += 1
        # d, calculated_rank, score_info = get_final_rank(data, product_rank_dict, 0.01, 0.49, 0.01, 0.49)
        d, calculated_rank, score_info = get_final_rank(data, product_rank_dict, best_sub, best_like, best_view, best_pos)
        print("Data size: ", len(data), "Kendall-tau distance: ", d)
    
def main():
    # store the database as a dict into a variable called product_info
    
    with open("final.json", "r") as file:
        product_info = json.load(file)

    product_sales_info = []
    for key, value in product_info.items():
        love = value.get('love', 1)
        star = value.get('star', 1)
        if love is None:
            love = 1
        if star is None:
            star = 1
        # if value['love'] == None:
        #     value['love'] = 1
        # if value['star'] == None:
        #     value['star'] = 1
        product_sales_info.append([key, (love * star / 5)])
    sorted_product_rank = sorted(product_sales_info, key=lambda x: x[1], reverse=True)
    product_rank_dict = {}
    i = 0
    for item in sorted_product_rank:
        product_rank_dict[item[0]] = i
        i += 1
    train_size = int(len(sorted_product_rank))
    train_data = product_info
    
    best_sub, best_like, best_view, best_pos = train(train_data, product_rank_dict)
    print("Best subscriber param: ", best_sub, "Best likes param: ", best_like, "Best views param: ", best_view, "Best pos param: ", best_pos)
    d, calculated_rank, score_info = get_final_rank(train_data, product_rank_dict, best_sub, best_like, best_view, best_pos)
    with open("score_list.json", "w") as file:
        json.dump(score_info, file)
    evaluate(product_info, best_sub, best_like, best_view, best_pos)
if __name__ == "__main__":
    main()


    