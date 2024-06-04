import requests
import json
from pymongo import MongoClient


class Mixpeek:
    def __init__(self):
        self.headers = {
            'Authorization': 'Bearer ',
            'Content-Type': 'application/json'
        }

        # Initialize MongoDB client
        self.client = MongoClient('')
        self.db = self.client['demos']
        self.collection = self.db['trump_transcripts']

    def insert(self, data):
        self.collection.insert_one(data)
        # print("Inserting data:", data)

    def embed(self, text):
        url = "http://localhost:8000/embed"
        payload = json.dumps({
            "input": text,
            "model": "jinaai/jina-embeddings-v2-base-en"
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)
        embedding = response.json()["embedding"]
        return embedding

    def process(self):
        url = "http://localhost:8000/extract"

        payload = json.dumps({
            "url": "https://static01.nyt.com/newsgraphics/documenttools/0ba92c46ef8b5337/8177c365-full.pdf"
        })
        response = requests.request("POST", url, headers=self.headers, data=payload)

        for chunk in response.json()["output"]:
            obj = {
                "embedding": self.embed(chunk['text']),
                "text": chunk['text'],
                "page": chunk['metadata']['page_number']
            }
            self.insert(obj)
            print("chunk_id: ", chunk['element_id'], "processed")


if __name__ == "__main__":
    # Create an instance of the Mixpeek class
    mixpeek_instance = Mixpeek()

    # Call the extract method to process the PDF
    mixpeek_instance.process()