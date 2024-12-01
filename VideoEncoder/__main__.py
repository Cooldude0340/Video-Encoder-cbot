# VideoEncoder - a telegram bot for compressing/encoding videos in h264/h265 format.
# Copyright (c) 2021 WeebTime/VideoEncoder
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from moviepy.editor import VideoFileClip

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the command handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Video Encoder Bot! Send me a video to encode.')

# Define the function to handle video messages
def handle_video(update: Update, context: CallbackContext) -> None:
    try:
        # Get the video file
        video_file = update.message.video.get_file()
        video_file.download('input_video.mp4')
        update.message.reply_text('Video received! Encoding...')

        # Encode the video
        encode_video('input_video.mp4', 'output_video.mp4')

        # Send the encoded video back to the user
        with open('output_video.mp4', 'rb') as video:
            update.message.reply_video(video)
        
        # Clean up files
        os.remove('input_video.mp4')
        os.remove('output_video.mp4')

    except Exception as e:
        logger.error(f"Error processing video: {e}")
        update.message.reply_text('An error occurred while processing your video. Please try again.')

# Function to encode the video
def encode_video(input_file: str, output_file: str) -> None:
    try:
        with VideoFileClip(input_file) as video:
            video.write_videofile(output_file, codec='libx264', audio_codec='aac')
    except Exception as e:
        logger.error(f"Error encoding video: {e}")
        raise

# Main function to start the bot
def main() -> None:
    # Replace 'YOUR_TOKEN' with your actual Telegram bot token
    updater = Updater("YOUR_TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.video, handle_video))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
