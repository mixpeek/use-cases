from mixpeek import Mixpeek
from pymongo import MongoClient

def create_mixpeek_client(api_key):
    return Mixpeek(api_key)

def get_database_collection(uri, db_name, collection_name):
    client = MongoClient(uri)
    return client[db_name][collection_name]

def process_video(mixpeek, video_url, frame_interval, resolution, return_base64):
    return mixpeek.tools.video.process(
        url=video_url,
        frame_interval=frame_interval,
        resolution=resolution,
        return_base64=return_base64
    )

def embed_video_chunks(mixpeek, processed_videos, video_url, collection):
    for index, video in enumerate(processed_videos):
        print(f"embedding video chunk: {index}")
        response = mixpeek.embed.video(
            model_id="mixpeek/vuse-generic-v1",
            input=video['base64_string'],
            input_type="base64"
        )
        obj = {
            "start_time": video['start_time'],
            "end_time": video['end_time'],
            "embedding": response['embedding'],
            "file_url": video_url
        }
        collection.insert_one(obj)

def search_video(mixpeek, video_url, collection):
    response = mixpeek.embed.video(
        model_id="mixpeek/vuse-generic-v1",
        input=video_url,
        input_type="url"
    )
    query = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": response['embedding'],
                "numCandidates": 10,
                "limit": 10
            }
        },
        {
            "$project": {
                "embedding": 0
            }
        }
    ]
    return list(collection.aggregate(query))

def main():
    api_key = 'sk-p21nNRv3P4Sbdzt1SCrgJMXWHiGPNpsd46VyojNEz5cznR1c3rP2L8KxSXbB2bsuzE8'
    mongo_uri = 'mongodb+srv://app:sYtMWBACfzcqsF2A@mixpeek.mhsby.mongodb.net'
    db_name = 'demos'
    collection_name = 'reverse_video_search'
    video_url = 'https://mixpeek-public-demo.s3.us-east-2.amazonaws.com/media-analysis/The+Third+Man++Official+Trailer.mp4'

    mixpeek = create_mixpeek_client(api_key)
    collection = get_database_collection(mongo_uri, db_name, collection_name)
    processed_videos = process_video(mixpeek, video_url, frame_interval=5, resolution=[720, 1280], return_base64=True)
    embed_video_chunks(mixpeek, processed_videos, video_url, collection)
    search_results = search_video(mixpeek, video_url, collection)
    print(search_results)

if __name__ == "__main__":
    main()