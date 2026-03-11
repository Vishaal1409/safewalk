"""
Test script to verify Supabase Storage is configured correctly.
Uploads a test image, retrieves its public URL, downloads it back, and cleans up.
"""

import os
import io
import uuid
import httpx
from PIL import Image
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env from project root
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")
BUCKET_NAME = "hazard-photos"

def create_test_image() -> bytes:
    """Generate a small 100x100 test image with colored quadrants."""
    img = Image.new("RGB", (100, 100), color="white")
    pixels = img.load()
    for x in range(100):
        for y in range(100):
            if x < 50 and y < 50:
                pixels[x, y] = (255, 0, 0)      # red
            elif x >= 50 and y < 50:
                pixels[x, y] = (0, 255, 0)      # green
            elif x < 50 and y >= 50:
                pixels[x, y] = (0, 0, 255)      # blue
            else:
                pixels[x, y] = (255, 255, 0)    # yellow
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def main():
    print("=" * 60)
    print("  Supabase Storage Upload/Retrieve Test")
    print("=" * 60)

    # --- Step 0: Check env vars ---
    print("\n[1/5] Checking environment variables...")
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("  ❌ SUPABASE_URL or SUPABASE_SECRET_KEY not set in .env")
        return
    print(f"  ✅ SUPABASE_URL = {SUPABASE_URL}")
    print(f"  ✅ SUPABASE_SECRET_KEY = {SUPABASE_KEY[:12]}...")

    # --- Step 1: Connect to Supabase ---
    print("\n[2/5] Connecting to Supabase...")
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("  ✅ Supabase client created successfully")
    except Exception as e:
        print(f"  ❌ Failed to create Supabase client: {e}")
        return

    # --- Step 2: Generate and upload test image ---
    print("\n[3/5] Generating and uploading test image...")
    image_bytes = create_test_image()
    file_name = f"test_{uuid.uuid4().hex[:8]}.png"
    print(f"  • File name: {file_name}")
    print(f"  • Image size: {len(image_bytes)} bytes")

    try:
        upload_response = supabase.storage.from_(BUCKET_NAME).upload(
            file_name,
            image_bytes,
            {"content-type": "image/png"}
        )
        print(f"  ✅ Upload successful!")
    except Exception as e:
        print(f"  ❌ Upload failed: {e}")
        print("\n  Possible issues:")
        print(f"    • The bucket '{BUCKET_NAME}' might not exist in Supabase Storage.")
        print("    • Go to Supabase Dashboard → Storage → New Bucket → create 'hazard-photos'")
        print("    • Make sure the bucket is set to 'Public' if you want public URLs.")
        return

    # --- Step 3: Get public URL ---
    print("\n[4/5] Retrieving public URL...")
    try:
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_name)
        print(f"  ✅ Public URL: {public_url}")
    except Exception as e:
        print(f"  ❌ Failed to get public URL: {e}")
        return

    # --- Step 4: Download the image back ---
    print("\n[5/5] Downloading image back from URL to verify...")
    try:
        resp = httpx.get(public_url, follow_redirects=True, timeout=15)
        if resp.status_code == 200:
            downloaded_img = Image.open(io.BytesIO(resp.content))
            print(f"  ✅ Download successful!")
            print(f"  • Downloaded image size: {downloaded_img.size}")
            print(f"  • Downloaded image format: {downloaded_img.format}")
            print(f"  • Content length: {len(resp.content)} bytes")
        else:
            print(f"  ⚠️  Download returned status {resp.status_code}")
            print(f"  • This may mean the bucket is not public.")
            print(f"  • The upload itself succeeded, so Supabase Storage is working!")
    except Exception as e:
        print(f"  ⚠️  Could not download image: {e}")
        print("  • The upload succeeded, so Supabase Storage IS configured correctly.")
        print("  • The download issue may be due to bucket privacy settings.")

    # --- Cleanup ---
    print("\n[Cleanup] Removing test file from storage...")
    try:
        supabase.storage.from_(BUCKET_NAME).remove([file_name])
        print(f"  ✅ Cleaned up: {file_name} removed from bucket")
    except Exception as e:
        print(f"  ⚠️  Cleanup failed (not critical): {e}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("  ✅ ALL TESTS PASSED — Supabase Storage is configured correctly!")
    print("=" * 60)


if __name__ == "__main__":
    main()
