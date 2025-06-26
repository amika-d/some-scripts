#!/usr/bin/env python3
"""
YouTube to MP3 Downloader
Downloads audio from YouTube videos and converts to MP3 format.
"""

import os
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Please install it using: pip install yt-dlp")
    sys.exit(1)

def get_download_path():
    """Get and validate the download path from user."""
    while True:
        path = input("Enter the absolute path where you want to save MP3 files: ").strip()
        
        if not path:
            print("Please enter a valid path.")
            continue
            
        # Convert to Path object and resolve
        download_path = Path(path).resolve()
        
        # Check if path exists
        if not download_path.exists():
            create = input(f"Path '{download_path}' doesn't exist. Create it? (y/n): ").strip().lower()
            if create in ['y', 'yes']:
                try:
                    download_path.mkdir(parents=True, exist_ok=True)
                    print(f"Created directory: {download_path}")
                except Exception as e:
                    print(f"Error creating directory: {e}")
                    continue
            else:
                continue
        
        # Check if it's a directory
        if not download_path.is_dir():
            print("The path must be a directory, not a file.")
            continue
            
        # Check if we can write to it
        if not os.access(download_path, os.W_OK):
            print("You don't have write permission to this directory.")
            continue
            
        return str(download_path)

def download_audio(url, download_path):
    """Download audio from YouTube URL and convert to MP3."""
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-ar', '44100'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            
            print(f"Title: {title}")
            if duration:
                mins, secs = divmod(duration, 60)
                print(f"Duration: {mins:02d}:{secs:02d}")
            
            # Download and convert
            print("Downloading and converting to MP3...")
            ydl.download([url])
            print(f"✓ Successfully downloaded: {title}")
            
    except Exception as e:
        print(f"✗ Error downloading {url}: {str(e)}")

def main():
    """Main function to run the downloader."""
    print("=== YouTube to MP3 Downloader ===")
    print("This script downloads audio from YouTube videos and converts them to MP3.")
    print("Press Enter without a URL to exit.\n")
    
    # Get download path
    download_path = get_download_path()
    print(f"Download path set to: {download_path}\n")
    
    # Check if ffmpeg is available
    try:
        import subprocess
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: FFmpeg not found. You may need to install FFmpeg for audio conversion.")
        print("Download from: https://ffmpeg.org/download.html\n")
    
    downloaded_count = 0
    
    # Main download loop
    while True:
        url = input("Enter YouTube URL (or press Enter to exit): ").strip()
        
        # Exit if empty input
        if not url:
            break
            
        # Basic URL validation
        if not any(domain in url.lower() for domain in ['youtube.com', 'youtu.be']):
            print("Please enter a valid YouTube URL.")
            continue
            
        print(f"\nProcessing: {url}")
        download_audio(url, download_path)
        downloaded_count += 1
        print("-" * 50)
    
    print(f"\nDownload session completed. Total files downloaded: {downloaded_count}")
    print("Thank you for using YouTube to MP3 Downloader!")

if __name__ == "__main__":
    main()