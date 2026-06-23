import hashlib

url = input("Enter URL: ")

short = hashlib.md5(
    url.encode()
).hexdigest()[:6]

print(
    "Short URL:",
    f"http://short.ly/{short}"
)
