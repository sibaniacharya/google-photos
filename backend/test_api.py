import urllib.request
import json

def test_endpoint(url, data=None):
    try:
        if data:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        else:
            req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {'error': str(e)}

print('--- Health Check ---')
print(test_endpoint('http://localhost:8000/health'))

print('\n--- Library Check ---')
library = test_endpoint('http://localhost:8000/api/retrieval/library')
print(f"Library size: {len(library.get('library', []))}")

print('\n--- Search Check ---')
search_data = {'memory': 'I remember a summer trip near the beach with friends. There was a yellow car and we had dinner around sunset.'}
search_res = test_endpoint('http://localhost:8000/api/retrieval/search', search_data)
print(json.dumps(search_res, indent=2))

print('\n--- Refine Check ---')
refine_data = {
    'previous_memory': search_data['memory'],
    'additional_memory': 'No, it was just Maya and me.'
}
refine_res = test_endpoint('http://localhost:8000/api/retrieval/refine', refine_data)
print(json.dumps(refine_res, indent=2))
