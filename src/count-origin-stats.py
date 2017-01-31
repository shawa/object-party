import sys
import json
from collections import defaultdict

input_data = json.load(sys.stdin)

resp_bytes = defaultdict(int)
occurences = defaultdict(int)
seen_domains = set()

for obj in input_data['objects']:
    domain = obj['url']
    resp_bytes[domain] += obj['bytes']
    occurences[domain] += 1
    seen_domains.add(domain)

object_stats = [{
    'domain': domain,
    'count': occurences[domain],
    'bytes': resp_bytes[domain],
    } for domain in seen_domains
]

output = {
    'domain': input_data['domain'],
    'objects': object_stats
}

json.dump(output, sys.stdout)
