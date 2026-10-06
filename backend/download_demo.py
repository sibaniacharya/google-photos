import urllib.request
import os

urls = {
    "photo_001.jpg": "https://lh3.googleusercontent.com/aida-public/AB6AXuBVj7XQzaMcb5gNYTRCgj5hyOzIfkXjM-h4yX6CRwsfY3bDzQzqj2Davz5pQO6XDiTi_aOa2TSYGCXlX3y8Gt2m7FBLME2niASG-mXS39EgeeYoQQU8izxD__3d6StVdorYshfR-1vHtw8Yug16F9CkpiRYFg_mGQDH5agXYC6Ge7QQAArnGHKwNAunT6I63jz5edHEGn3qNUfjmyr8c7kat5n0jWQalXRjddjfuFRpf_04buGnwzwt",
    "photo_002.jpg": "https://lh3.googleusercontent.com/aida-public/AB6AXuDteHX-alhOC1P2LO3n_i3Kv4hYRzmTi4c26VSrOG_t4CIPuxi3evNtfaBbM57dpzTGCLBH24AqNjNS6Aceykk2IIb21dYJix0SBxdC4eaFCweuRW5GatdP-5hfxhW7NKQlPfY5Pl8uQQAuiJAaFjCeqpnJ8Bp4IMe_GsX3AiQiLdbtC90K5O78JGSFjhGxoIpZm6DamPreOfKwPvuE4v7I0rQPla4bkEVXZrctJ2_ODH03UlI0C3EQ",
    "photo_003.jpg": "https://lh3.googleusercontent.com/aida-public/AB6AXuCTwIKuM8PlmaEDwt837RtjX_2jixec8kZjLOZOxWLtFSbvEV6qe89us1XvHRK4BMf5RXSyTDsobdM9c3uyCL5ITWf4usZfmskzr-MjqnYU7ApMuorVKnLzrDo8sACsbsuq0GFyg2BthanyuD_TBNX8_wl0Rl7M2woOqTPM6hK0so1lcXKfanpIfRD5P0Zmx1dFBUA61DR74PCsuQm0jioR5oBRTju_vfhFpsvun7lzEsZCq9LaZ55x"
}

out_dir = r"c:\Users\siban\OneDrive\Desktop\NextLeap\Graduation Project\Second Attempt\Google photos\frontend\public\demo-photos"
os.makedirs(out_dir, exist_ok=True)

for name, url in urls.items():
    print(f"Downloading {name}...")
    try:
        urllib.request.urlretrieve(url, os.path.join(out_dir, name))
        print(f"Downloaded {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
