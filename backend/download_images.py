import urllib.request
import os
import ssl
import time

# Disable SSL verification for simple script
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "public", "demo-photos")
os.makedirs(output_dir, exist_ok=True)

print(f"Downloading 50 actual placeholder images to {output_dir}")

for i in range(1, 51):
    filename = f"photo_{i:03d}.jpg"
    filepath = os.path.join(output_dir, filename)
    url = f"https://picsum.photos/seed/memsearch{i}/800/600"
    
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"Downloaded {filename}")
        time.sleep(0.5) # Be nice to the API
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

print("Done downloading images.")
