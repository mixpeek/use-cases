# Install necessary packages
!pip install mixpeek pymongo

# Import necessary libraries
from mixpeek import Mixpeek
from pymongo import MongoClient

# Initialize Mixpeek client and MongoDB collection
api_key = ''
mongo_uri = ''
db_name = 'demos'
collection_name = 'reverse_video_search'

mixpeek = Mixpeek(api_key)
collection = MongoClient(mongo_uri)[db_name][collection_name]

# Process video
video_index_url = 'https://mixpeek-public-demo.s3.us-east-2.amazonaws.com/media-analysis/The+Third+Man++Official+Trailer.mp4'
processed_videos = mixpeek.tools.video.process(
    url=video_index_url,
    frame_interval=20,
    resolution=[720, 1280],
    return_base64=True
)

# Embed video chunks and insert into MongoDB
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
        "file_url": video_index_url
    }
    collection.insert_one(obj)

# Perform a reverse video search and display results
response = mixpeek.embed.video(
    model_id="mixpeek/vuse-generic-v1",
    input="https://mixpeek-public-demo.s3.us-east-2.amazonaws.com/media-analysis/video_queries/exiting_sewer.mp4",
    input_type="url"
)

query = [
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": response['embedding'],
            "numCandidates": 10,
            "limit": 3
        }
    },
    {
        "$project": {
            "embedding": 0
        }
    }
]

search_results = list(collection.aggregate(query))
print(search_results)