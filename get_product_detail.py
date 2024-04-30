from bs4 import BeautifulSoup
import requests
import re
from PIL import Image
from collections import Counter
from io import BytesIO
import json
from colormath.color_objects import sRGBColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor
import numpy as np
from colormath.color_conversions import convert_color
from urllib.parse import urlparse, parse_qs
# For the use of delta_e_cie2000
def patch_asscalar(a):
    return a.item()

setattr(np, "asscalar", patch_asscalar)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
} 

# The function for crawling Sephora data
def get_product_detail(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    with open ("product_info_1.txt", 'w') as f:
        f.write(soup.prettify())
    
    # Initialize
    price = None
    benefits = []
    img_url = None
    reviews = None
    love = None
    star = None
    colorImg = None
    color_label = None

    # Price
    target_html = soup.find('span', class_='css-18jtttk')
    pattern = re.compile(r'\$(\d+\.\d+)')
    if target_html:
        match = re.search(pattern, target_html.get_text())
        if match:
            price = float(match.group(1))

    # Benefit
    get_benefit("Long-wearing", soup, benefits)
    get_benefit("Hydrating", soup, benefits)
    get_benefit("Plumping", soup, benefits)
    get_benefit("Transfer-resistant", soup, benefits)
    get_benefit("Transfer-proof", soup, benefits)
    get_benefit("Waterproof", soup, benefits)

    # Name
    name_html = soup.find('title')
    name = name_html.get_text()
    name = name.replace(" | Sephora", "")

    # Reviews number
    reviews_html = soup.find('span', class_='css-1j53ife')
    if reviews_html:
        reviews_text = reviews_html.get_text()
        pattern = re.compile(r'(\d+(?:\.\d+)?)')
        match = re.search(pattern, reviews_html.get_text())
        if match:
            reviews = float(match.group(1))
            if reviews_text[-1] == 'K':
                reviews = reviews * 1000
            if reviews_text[-1] == 'M':
                reviews = reviews * 1000000

    # Love number
    love_html = soup.find('span', class_='css-jk94q9')
    if love_html:
        love_text = love_html.get_text()
        pattern = re.compile(r'(\d+(?:\.\d+)?)')
        match = re.search(pattern, love_html.get_text())
        if match:
            love = float(match.group(1))
            if love_text[-1] == 'K':
                love = love * 1000
            if love_text[-1] == 'M':
                love = love * 1000000

    # Star ratings
    star_html = soup.find('span', class_='css-1tbjoxk')
    if star_html:
        star = star_html.get('aria-label')
        parts = star.split()
        rating = parts[0]
        star = float(rating)

    # Product Color
    parsed_url = urlparse(url)

    # Get the query parameters
    query_params = parse_qs(parsed_url.query)

    # Get the value of the "skuld" parameter
    skuid = query_params.get('skuId', [''])[0]
    print("skuld", skuid)
    colorImg = f"https://www.sephora.com/productimages/sku/s{skuid}+sw.jpg"

    print("Modified URL:", img_url)

    # Product Image Url
    target_html = soup.find('img', class_='css-1rovmyu eanm77i0')
    if target_html:
        img_url = target_html.get('src')
        img_url = f"https://www.sephora.com/productimages/sku/s{skuid}-main-hero.jpg"
    # Get the main color of the image
    color_rgb = get_image_color(colorImg)
    if color_rgb:
        # Get the label of the color
        color_label = get_color_label(color_rgb)

    lips_info = {"name": name, "colorCat": "red", "colorCat": color_label, "colorImg": colorImg, "benefitCat": benefits, "price": price,  "imagePath": img_url, "reviews": reviews, "love": love, "star": star}
    return lips_info
    



# Get the most frequent color of the image
def get_image_color(image_url):
    # Open the image
    response = requests.get(image_url, headers=headers)
    most_common_color = None
    if response.status_code == 200:
        print(response)
        img = Image.open(BytesIO(response.content))
        
        # Convert the image to RGB mode
        img = img.convert('RGB')
        pixel_colors = list(img.getdata())
        # Count occurrences of each color
        color_counts = Counter(pixel_colors)
        # Find the most common color
        most_common_color = color_counts.most_common(1)[0][0]
    return most_common_color

# Label RGB color to one category
def get_color_label(color_rgb):
    colors = None
    with open('color.json') as f:
        colors = json.load(f)
    color_rgb = tuple(float(x)/255 for x in color_rgb)
    # Calculate the Delta E (CIE 2000) between the two colors
    product_color_rgb = sRGBColor(*color_rgb)
    product_color_rgb = convert_color(product_color_rgb, LabColor)
    min_delta_e = 100
    label = None
    for key, color in colors.items():
        color_rgb = color['rgb'] 
        color_rgb = [float(x)/255 for x in color_rgb]
        label_color_rgb = sRGBColor(*color_rgb)
        label_color_rgb = convert_color(label_color_rgb, LabColor)
        delta_e = delta_e_cie2000(product_color_rgb, label_color_rgb)
        if delta_e < min_delta_e:
            min_delta_e = delta_e
            label = key
    return label


def get_benefit(text, soup, benefits):
    match = re.search(text, soup.prettify())
    if match:
        benefits.append(text)
    

if __name__ == "__main__":
    # For testing
    res = get_product_detail("https://www.sephora.com/product/huda-beauty-faux-filler-shiny-non-sticky-lip-gloss-P509453?skuId=2739480&icid2=products%20grid:p509453:product")
    print(res)
