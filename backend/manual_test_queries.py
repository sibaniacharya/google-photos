import urllib.request
import json
import time

def call_api(endpoint, data):
    url = f"http://localhost:8000/api/retrieval/{endpoint}"
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

queries = [
    "I remember a beach trip with friends around summer, probably near sunset.",
    "I remember a birthday dinner with family, but I don't remember the date.",
    "I remember a photo with a yellow car near the sea.",
    "I remember an old family photo indoors but I don't remember exactly when.",
    "I remember a road trip with friends and a mountain view."
]

print("--- Running tests ---")

# TEST 1
print("\n--- TEST 1 ---")
res1 = call_api("search", {"memory": queries[0]})
print("Cues extracted:")
print(json.dumps(res1["cues"], indent=2))
print("Top candidate:")
if res1["candidates"]:
    print(res1["candidates"][0]["match_level"], res1["candidates"][0]["reason"])

# TEST 2 (Refinement of Test 1)
print("\n--- TEST 2 (Refine Test 1) ---")
res2 = call_api("refine", {
    "previous_cues": res1["cues"],
    "additional_memory": "I don't remember when.",
    "rejected_candidate": res1["candidates"][0]["photo_id"] if res1["candidates"] else None
})
print("Updated Cues extracted:")
print(json.dumps(res2["cues"], indent=2))
print("Top candidate:")
if res2["candidates"]:
    print(res2["candidates"][0]["match_level"], res2["candidates"][0]["reason"])

# TEST 3, 4, 5, 6
for i, q in enumerate(queries[1:]):
    print(f"\n--- TEST {i+3} ---")
    res = call_api("search", {"memory": q})
    print("Query:", q)
    print("Cues extracted:")
    print(json.dumps(res["cues"], indent=2))
    print("Top candidate:")
    if res["candidates"]:
        print(res["candidates"][0]["match_level"], res["candidates"][0]["reason"])
