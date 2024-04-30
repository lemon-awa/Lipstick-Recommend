import json

with open('src/score_list.json', 'r') as f:
    data = json.load(f)

# Initialize an array to store the formatted data
initialFacts = []
all_benefits = set()
count=0

# Iterate over each item in the JSON file
for key, value in data.items():
    # Extract relevant information
    name = value['name']
    source = value['source']
    colorCat = value['colorCat']
    benefitCat = value['benefitCat']
    price = '${:.1f}'.format(value['price'])  # Format price to two decimal places
    imagePath = value['imagePath']
    colorImg = value['colorImg']
    # score = round(value['star'])  # Round star rating to the nearest integer
    score = value['score']

    for b in benefitCat:
        all_benefits.add(b)

    priceCat = "Under $25"
    p = value['price']
    if p >= 25:
        priceCat="$25 to $50"

    if p >=50:
        priceCat = "$50 to $100"

    if p >= 100:
        priceCat="$100 and above"

    if not colorCat:
        continue

    # Create a dictionary for the item
    item = {
        'id':count+1,
        'name': name,
        'source': source,
        'colorCat': colorCat,
        'benefitCat': benefitCat,
        'price': price,
        'priceCat': priceCat,
        'imagePath': imagePath,
        'score': score,
        'colorImg': colorImg,
    }

    count += 1

    # Append the item to the array
    initialFacts.append(item)

# Print the formatted array
print(initialFacts)
# print(all_benefits)
