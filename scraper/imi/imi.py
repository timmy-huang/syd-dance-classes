import requests

# pre sure these guys use square space

# They seem to use a widget within their squarespace called mindbody which is some sort of scheduling software
# We can use their js call "load_markup" to get the data
# /widgets/schedules/86397/load_markup?callback=jQuery36408016788701280633_1713673043345&options%5Bstart_date%5D=2024-04-21&_=1713673043348

# curl ^"https://widgets.mindbodyonline.com/widgets/schedules/86397/load_markup?callback=jQuery36408016788701280633_1713673043345&options^%^5Bstart_date^%^5D=2024-04-21&_=1713673043348^" ^
#   -H "accept: */*" ^
#   -H "accept-language: en-US,en;q=0.9" ^
#   -H "referer: https://imient.com.au/" ^
#   -H ^"sec-ch-ua: ^\^"Google Chrome^\^";v=^\^"123^\^", ^\^"Not:A-Brand^\^";v=^\^"8^\^", ^\^"Chromium^\^";v=^\^"123^\^"^" ^
#   -H "sec-ch-ua-mobile: ?1" ^
#   -H ^"sec-ch-ua-platform: ^\^"Android^\^"^" ^
#   -H "sec-fetch-dest: script" ^
#   -H "sec-fetch-mode: no-cors" ^
#   -H "sec-fetch-site: cross-site" ^
#   -H "user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"

r = requests.get('https://imient.com.au/classes')
print(r.text)
# Save to a file
with open('imi.txt', 'w', encoding='utf-8') as f:
    f.write(r.text)
  
