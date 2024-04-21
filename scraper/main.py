import requests

r = requests.get('https://www.movementnation.com.au/hurstville-bookings')
print(r.text)
print("hi")
# Save to a file
with open('movement-hurssie.txt', 'w', encoding='utf-8') as f:
    f.write(r.text)
    