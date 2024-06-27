# Media Analysis Demo Using Mixpeek's Video Embedding API

This demo showcases how to use Mixpeek's Video Embedding API to analyze movie trailers. The process involves downloading trailers from YouTube, uploading them to a storage service, and then using Mixpeek to process and embed the videos for further analysis.

## Components

- **download.py**: Script to download movie trailers from YouTube and upload them to a storage service.
- **index.py**: Script to process the uploaded videos using Mixpeek's Video Embedding API and store the embeddings in a MongoDB database.
- **movies.json**: JSON file containing metadata of movies including titles, directors, years, and trailer URLs.
- **requirements.txt**: Contains the Python packages required for the project.

## Setup

1. **Python Environment**: Ensure Python 3.8+ is installed on your system.
2. **Dependencies**: Install the required Python packages using:
   ```bash
   pip install -r requirements.txt
   ```
3. **API Keys and Database**: You will need to replace placeholders in the scripts with your actual Mixpeek API key, MongoDB URI, and other configuration details.

## Usage

### Step 1: Download and Upload Trailers

Run the `download.py` script to download trailers from YouTube and upload them to your specified storage. This script updates the MongoDB database with the URLs of the uploaded videos.

```bash
python download.py
```

### Step 2: Process Videos and Embed

Execute the `index.py` script to process the videos using Mixpeek's API and store the video embeddings in the database.

```bash
python index.py
```

## Files Description

- **download.py**: Handles the downloading of YouTube trailers and uploading to a cloud storage. It also updates the database with the URLs of the uploaded videos.
- **index.py**: Processes each video to extract embeddings and stores these embeddings along with additional metadata in the MongoDB database.
- **movies.json**: Provides a list of movies with essential details used by the `download.py` script.
- **requirements.txt**: Lists all the necessary Python libraries that need to be installed.

This demo provides a comprehensive example of how to integrate various APIs and services for a media analysis application.
