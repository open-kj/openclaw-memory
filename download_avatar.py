import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Try Pexels free professional headshots
urls = [
    ("https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=400", "ai_avatar.jpg"),
    ("https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=400", "ai_avatar.jpg"),
    ("https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&w=400", "ai_avatar.jpg"),
]

output_base = r"C:\Users\Administrator\Desktop\ceshi"

for url, fname in urls:
    try:
        print(f"Trying: {url[:60]}...")
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'image/*'
        })
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = resp.read()
            if len(data) > 10000:  # Need at least 10KB
                output = rf"{output_base}\{fname}"
                with open(output, 'wb') as f:
                    f.write(data)
                print(f"Success! {len(data)} bytes -> {output}")
                break
            else:
                print(f"Too small: {len(data)} bytes")
    except Exception as e:
        print(f"Failed: {e}")
