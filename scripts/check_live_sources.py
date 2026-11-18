import urllib.request
import json

def check():
    req = urllib.request.urlopen('http://127.0.0.1:8000/api/v1/intelligence/sources')
    sources = json.loads(req.read().decode('utf-8'))
    print(f'Total Registered External Streams: {len(sources)}')
    for s in sources:
        print(f"  * {s['name']} [ID: {s['source_id']}]")
        print(f"    - Endpoint: {s['endpoint']}")
        print(f"    - Health: {s['health_status']}")
        print(f"    - Freshness: {s['freshness_status']} (Age: {s['age_human']}, Stale: {s['is_stale']})")
        print(f"    - Response Time: {s['response_time_ms']} ms")
        print(f"    - Frequency: {s['update_frequency']}")
        print(f"    - Last Checked: {s['last_checked']}")
        print(f"    - Last Success: {s['last_success']}\n")

    req2 = urllib.request.urlopen('http://127.0.0.1:8000/api/v1/intelligence/freshness')
    fresh = json.loads(req2.read().decode('utf-8'))
    print(f"Summary Freshness: {fresh['fresh_sources']} Fresh, {fresh['acceptable_sources']} Acceptable, {fresh['stale_sources']} Stale, {fresh['unavailable_sources']} Unavailable")

if __name__ == '__main__':
    check()
