from pymongo import MongoClient
import requests
import json

class VideoProcessor:
    def __init__(self, db_uri, db_name, collection_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.process_url = "https://api.mixpeek.com/tools/video/process"
        self.embed_url = "https://api.mixpeek.com/embed"
        self.headers = {
            'Authorization': 'Bearer ',
            'Content-Type': 'application/json'
        }

    def process_video(self, video_file_url):
        process_payload = json.dumps({
            "url": video_file_url,
            "frame_interval": 5,
            "resolution": [720, 1280],
            "use_base64": True
        })

        response = requests.request("POST", self.process_url, headers=self.headers, data=process_payload)
        process_data = response.json()

        for chunk in process_data:
            self._embed_and_store(chunk, video_file_url)

    def _embed_and_store(self, chunk, video_file_url):
        embed_payload = json.dumps({
            "input": chunk['file_url'],
            "modality": "video",
            "model": "mixpeek/vuse-generic-v1",
            "input_type": "base64"
        })

        response = requests.request("POST", self.embed_url, headers=self.headers, data=embed_payload)
        embed_data = response.json()['embedding']

        document = {
            'file_url': video_file_url,
            'start_time': chunk['start_time'],
            'end_time': chunk['end_time'],
            'fps': chunk['fps'],
            'duration': chunk['duration'],
            'resolution': chunk['resolution'],
            'size_kb': chunk['size_kb'],
            'embedding': embed_data
        }

        self.collection.insert_one(document)

class VectorSearch:
    def __init__(self, db_uri, db_name, collection_name):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def _embed(self, text): 
        self.embed_url = "https://api.mixpeek.com/embed"
        self.headers = {
            'Authorization': 'Bearer ',
            'Content-Type': 'application/json'
        }
        embed_payload = json.dumps({
            "input": text,
            "modality": "video",
            "model": "mixpeek/vuse-generic-v1",
            "input_type": "text"
        })

        response = requests.request("POST", self.embed_url, headers=self.headers, data=embed_payload)
        return response.json()['embedding']

    def search_by_embedding(self, embedding_vector, max_results=10):
        query = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": embedding_vector,
                "numCandidates": 10,
                "limit": 10
            }
        },
        {
            "$project": {
                "embedding": 0,
                # "start_time": 1,
                # "end_time": 1,
            }
        }
        ]
        return list(self.collection.aggregate(query))
    


# Initialize the VideoProcessor with MongoDB connection details
db_uri = ""
db_name = "demos"
collection_name = ""

# video_processor = VideoProcessor(db_uri, db_name, collection_name)

# # URL of the video to be processed
# video_file_url = "http://example.com/path/to/video.mp4"

# # Process the video
# video_processor.process_video(video_file_url)

# Initialize the VectorSearch
vector_search = VectorSearch(db_uri, db_name, collection_name)

# Example embedding vector (you would get this from actual data or test data)
embedding_vector = vector_search._embed("falling on the floor")

# Search for similar videos
results = vector_search.search_by_embedding(embedding_vector)

# Print the results
# Pretty print the results with indents
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(results)