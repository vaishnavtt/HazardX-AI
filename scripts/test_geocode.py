import urllib.request
import urllib.parse
import json

queries = ['Wayanad', 'Koch', 'London', 'Tokyo', '29.95,-90.07']
for q in queries:
    url = f"http://127.0.0.1:8000/api/v1/geospatial/geocode?q={urllib.parse.quote(q)}"
    res = urllib.request.urlopen(url)
    data = json.loads(res.read().decode())
    print(f"Query: '{q}' -> Count: {data['count']}")
    for r in data['results'][:2]:
        print(f"   * {r['name']} ({r['country']}) -> Lat: {r['latitude']}, Lon: {r['longitude']}")
    print()
