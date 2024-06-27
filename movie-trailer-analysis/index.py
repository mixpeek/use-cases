import json
import os
from youtubesearchpython import VideosSearch
from pytube import YouTube
from mixpeek import Mixpeek
import pymongo  # Import pymongo for MongoDB interactions

# Initialize the Mixpeek client with your API key
mixpeek = Mixpeek('YOUR_MIXPEEK_API_KEY')

# MongoDB connection setup
client = pymongo.MongoClient("YOUR_MONGODB_URI")
db = client["your_database_name"]
collection = db["your_collection_name"]

# Load all movies into memory
movies = list(collection.find().sort("rank", pymongo.DESCENDING))

# Process each movie
for movie in movies:
    try:
        processed_videos = mixpeek.tools.video.process(
            url=movie['full_url'],
            frame_interval=5,
            resolution=[720, 1280],
            return_base64=True
        )

        embeddings_to_insert = []
        for index, video in enumerate(processed_videos):
            print(f"embedding video chunk: {index}")
            embed_response = mixpeek.embed.video(
                model_id="YOUR_MODEL_ID",
                input=video['base64_string'],
                input_type="base2"
            )
            video.pop('base64_string')
            video['file_url'] = movie['full_url']
            embeddings_to_insert.append({
                "embedding": embed_response['embedding'],
                **video,
                "movie_info": movie
            })

        # Insert all embeddings for the current movie at once
        if embeddings_to_insert:
            db.movie_embeddings.insert_many(embeddings_to_insert)

    except Exception as e:
        print(f"Failed to process {movie['title']}: {e}")