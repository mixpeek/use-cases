import json
import os
from youtubesearchpython import VideosSearch
from pytube import YouTube
from mixpeek import Mixpeek
import pymongo  # Import pymongo for MongoDB interactions

# Initialize the Mixpeek client with your API key
mixpeek = Mixpeek('YOUR_MIXPEEK_API_KEY')

def get_youtube_trailer_url(query):
    videos_search = VideosSearch(query, limit=1)
    return videos_search.result()["result"][0]["link"]

def download_youtube_video(url, title):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream.download(filename=f"{title}.mp4")
    return f"{title}.mp4"

def main():
    # MongoDB connection setup
    client = pymongo.MongoClient("YOUR_MONGODB_URI")
    db = client["your_database_name"]
    collection = db["your_collection_name"]
    
    for movie in collection.find():  # Iterate through documents in the MongoDB collection
        print(f"Processing movie: {movie['title']}")
        try:
            video_path = download_youtube_video(movie["trailer_url"], movie["title"])
            response = mixpeek.connections.storage.upload(
                connection_id="YOUR_CONNECTION_ID",
                file_path=video_path,
                prefix="movies"
            )
            print(f"Upload successful: {response}")            
            collection.update_one({"_id": movie["_id"]}, {"$set": {"full_url": response["full_url"]}})
            os.remove(video_path)
        except Exception as e:
            print(f"Failed to process {movie['title']}: {e}")

if __name__ == "__main__":
    main()