import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to fetch images from Wikipedia page
def search(url):
    # Create folder to save images
    HEADERS = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                }

    # url = f"https://en.wikipedia.org/wiki/{url}"
    # url = f"https://unsplash.com/s/photos/{url}"
    url = f"https://www.flickr.com/search/?text={url}"
    response = requests.get(url , headers = HEADERS)

    # Check if the correct encoding is detected
    if response.encoding is None:
        response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')

    # Fetching all image src attributes
    imagesData = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]

    output = []
    for index, img_url in enumerate(imagesData):
        # Handle relative URLs by converting them to absolute URLs
        if not img_url.startswith("http"):
            img_url = requests.compat.urljoin(url, img_url)

        output.append(img_url)

    return output

# Route for searching and downloading images
@app.route('/', methods=['POST'])
def search_image():
    query = request.json
    if 'query' not in query:
        return jsonify({"error": "Query parameter missing"}), 400

    search_term = query['query']
    result = search(search_term)

    return jsonify({"images": result,"count":len(result)})

# Test route
@app.route('/', methods=['GET'])
def main():
    return send_from_directory('static' , 'index.html')

if __name__ == '__main__':
    app.run(debug=False , port=4000)
