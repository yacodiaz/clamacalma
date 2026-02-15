import argparse
import os
import re
import sys
import time
import unicodedata

import instaloader


def sanitize_folder_name(name):
    """Clean a caption's first line into a valid folder name."""
    # Remove emojis and special unicode characters, keep letters/numbers/spaces
    cleaned = ""
    for ch in name:
        cat = unicodedata.category(ch)
        if cat.startswith("So") or cat.startswith("Sk") or cat.startswith("Cn"):
            continue  # skip symbols/emojis
        cleaned += ch
    # Remove hashtags and mentions
    cleaned = re.sub(r"[#@]\S+", "", cleaned)
    # Remove invalid filename characters
    cleaned = re.sub(r'[<>:"/\\|?*]', "", cleaned)
    # Collapse whitespace, strip, lowercase
    cleaned = re.sub(r"\s+", " ", cleaned).strip().lower()
    # Cap length
    if len(cleaned) > 60:
        cleaned = cleaned[:60].rstrip()
    return cleaned


def get_game_name(post):
    """Extract the game/product name from the post caption."""
    caption = post.caption
    if not caption or not caption.strip():
        return None

    first_line = caption.strip().split("\n")[0].strip()

    # Skip posts that are clearly not product posts
    skip_patterns = [
        r"^#\w+",                    # starts with hashtag
        r"(?i)sorteo",               # giveaway
        r"(?i)feria",                # fair/market
        r"(?i)feliz dia",            # greetings
        r"(?i)es hoy",               # event announcements
        r"(?i)ultimo dia",           # last day announcements
        r"(?i)los domingos",         # schedule posts
    ]
    for pattern in skip_patterns:
        if re.search(pattern, first_line):
            return None

    name = sanitize_folder_name(first_line)
    if not name or len(name) < 3:
        return None

    return name


def main():
    parser = argparse.ArgumentParser(
        description="Download photos from a public Instagram profile, organized by product name."
    )
    parser.add_argument("username", help="Public Instagram username")
    parser.add_argument("--output", default="./downloads", help="Output directory (default: ./downloads)")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between downloads in seconds (default: 2.0)")
    args = parser.parse_args()

    username = args.username
    base_dir = os.path.join(args.output, username)
    otros_dir = os.path.join(base_dir, "otros")

    loader = instaloader.Instaloader(
        download_videos=False,
        download_video_thumbnails=False,
        download_comments=False,
        save_metadata=False,
        post_metadata_txt_pattern="",
        filename_pattern="{date_utc}__{shortcode}",
    )

    try:
        print(f"Fetching profile: {username}")
        profile = instaloader.Profile.from_username(loader.context, username)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Error: Profile '{username}' does not exist.")
        sys.exit(1)
    except instaloader.exceptions.ConnectionException as e:
        print(f"Error: Could not connect to Instagram. {e}")
        sys.exit(1)

    if profile.is_private:
        print(f"Error: Profile '{username}' is private.")
        sys.exit(1)

    post_count = profile.mediacount
    print(f"Found {post_count} posts. Organizing photos by game name into: {base_dir}")
    print(f"Delay between downloads: {args.delay}s")
    print()

    downloaded = 0
    skipped_videos = 0
    errors = 0
    folders_used = {}

    try:
        for i, post in enumerate(profile.get_posts(), 1):
            if post.is_video:
                skipped_videos += 1
                print(f"[{i}/{post_count}] Skipping video {post.shortcode}")
                continue

            game_name = get_game_name(post)
            if game_name:
                target_dir = os.path.join(base_dir, game_name)
            else:
                target_dir = otros_dir
                game_name = "otros"

            os.makedirs(target_dir, exist_ok=True)
            folders_used[game_name] = folders_used.get(game_name, 0) + 1

            try:
                print(f"[{i}/{post_count}] -> {game_name}/ : {post.shortcode}...", end=" ", flush=True)
                loader.download_post(post, target=target_dir)
                downloaded += 1
                print("OK")
            except instaloader.exceptions.ConnectionException as e:
                errors += 1
                print(f"FAILED ({e})")
                # Wait longer on connection errors (rate limiting)
                time.sleep(args.delay * 3)

            time.sleep(args.delay)

    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
    except instaloader.exceptions.ConnectionException as e:
        print(f"\nConnection error (possible rate limit): {e}")

    print(f"\n{'=' * 50}")
    print(f"Downloaded: {downloaded} | Videos skipped: {skipped_videos} | Errors: {errors}")
    print(f"\nFolders created:")
    for folder, count in sorted(folders_used.items()):
        print(f"  {folder}: {count} photos")


if __name__ == "__main__":
    main()
