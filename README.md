*# Video Search and Upload Bot

A Python-based bot that automates downloading videos from platforms like Instagram and TikTok and uploads them to a server using API integration.

##  Features
- Search and download videos from specified platforms.
- Upload videos to a server using a pre-signed URL.
- Automatically delete local files after successful uploads.
- Monitor the /videos directory for new .mp4 files and process them automatically.
- Asynchronous operations for high performance.

##  Requirements
1. *Python* 3.8 or higher.
2. *Flic-Token*:  
   - Message the official Empowerverse bot on Telegram with your Empowerverse username to obtain the token.
3. *Python Dependencies*:  
   - Install required libraries using the command:
     bash
     pip install -r requirements.txt
     

## Project Structure

video-bot/ ├── main.py                # Main script containing the bot logic ├── requirements.txt       # Python dependencies └── README.md              # Project documentation

## ⚙ How to Use

### 1. Clone the Repository
```bash
git clone <repository-url>
cd video-bot

2. Install Dependencies

pip install -r requirements.txt

3. Configure the Token

Replace <YOUR_FLIC_TOKEN> in main.py with the Flic-Token you received from the Empowerverse bot on Telegram.

4. Run the Bot

python main.py

5. Add Videos

Place .mp4 video files into the /videos directory. The bot will automatically process and upload them.

API Integration

The bot interacts with the following APIs:

1. Generate Upload URL

Endpoint: https://api.socialverseapp.com/posts/generate-upload-url

Method: GET

Headers:

Flic-Token: <YOUR_FLIC_TOKEN>
Content-Type: application/json



2. Upload Video

Method: PUT

Uses the pre-signed URL obtained from the Generate Upload URL API.



3. Create Post

Endpoint: https://api.socialverseapp.com/posts

Method: POST

Headers:

Flic-Token: <YOUR_FLIC_TOKEN>
Content-Type: application/json

Body:

{
    "title": "<video title>",
    "hash": "<hash_from_step_1>",
    "is_available_in_public_feed": false,
    "category_id": <category_id>
}




Notes

Ensure your Python environment is set up with the required libraries.

Handle the Flic-Token securely and do not share it publicly.

The bot only processes .mp4 files in the /videos directory.


Support

For issues or feature requests, please contact the repository owner or reach out to Empowerverse support on Telegram.