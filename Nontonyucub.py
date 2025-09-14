import subprocess
import sys
import shutil
import json

def check_dependencies():
    # Check for mpv
    if shutil.which("mpv") is None:
        print("[!] 'mpv' is not installed. Please install it with: sudo apt install mpv")
        sys.exit(1)
    
    # Check for yt-dlp
    if shutil.which("yt-dlp") is None:
        print("[!] 'yt-dlp' is not installed. Installing via pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)

def search_youtube(query, max_results=3):
    print(f"[*] Searching YouTube for: {query}...")
    cmd = [
        "yt-dlp",
        f"ytsearch{max_results}:{query}",
        "--print", "%(title)s | %(duration_string)s | %(webpage_url)s",
        "--no-warnings",
        "--no-playlist"
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().split("\n")
    videos = []

    for line in lines:
        try:
            title, duration, url = map(str.strip, line.split("|", 2))
            videos.append({"title": title, "duration": duration, "url": url})
        except ValueError:
            continue

    return videos

def choose_video(videos):
    print("\n[✓] Search Results:")
    for i, video in enumerate(videos):
        print(f"{i+1}. {video['title']} ({video['duration']})")

    choice = input("\nEnter the number of the video to play (or press Enter to cancel): ")
    if not choice.isdigit():
        print("Cancelled.")
        sys.exit(0)

    index = int(choice) - 1
    if 0 <= index < len(videos):
        return videos[index]["url"]
    else:
        print("Invalid choice.")
        sys.exit(1)

def play_video(url):
    print(f"\n[*] Playing: {url}")
    subprocess.run(["mpv", "--ytdl-format=bestvideo+bestaudio", url])

def main():
    check_dependencies()
    query = input("Search YouTube: ").strip()
    if not query:
        print("No search query entered.")
        return

    videos = search_youtube(query)
    if not videos:
        print("No results found.")
        return

    url = choose_video(videos)
    play_video(url)

if __name__ == "__main__":
    main()
