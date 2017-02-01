import subprocess
import sys
import json
import re
from collections import defaultdict


def alternative_names(domain):
    '''
    for a given domain, return a set of all alternative names in its x509 cert
    '''
    try:
        alts = json.loads(subprocess.check_output(['./domain-alts.sh', domain]))
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Failed to load certs")
    return frozenset(alts["alts"])


def to_re(alternative_names):
    def _to_re_text(alt_name):
        return re.sub(r'^\*\.', r'.+\.', alt_name)

    domains_re = re.compile('|'.join(map(_to_re_text, alternative_names)))
    return re.compile(domains_re)


def count_size_and_occurences(filtered_har):
    first_party_name = filtered_har['domain']
    alts = alternative_names(first_party_name)
    alts_re = to_re(alts)

    resp_bytes = defaultdict(int)
    occurences = defaultdict(int)
    seen_domains = set()

    for obj in filtered_har['objects']:
        domain = obj['url']
        resp_bytes[domain] += obj['bytes']
        occurences[domain] += 1
        seen_domains.add(domain)

    object_stats = [{
        'domain': domain,
        'count': occurences[domain],
        'is_first_party': alts_re.match(domain) is not None,
        'bytes': resp_bytes[domain],
        } for domain in seen_domains
    ]

    output = {
        'domain': first_party_name,
        'objects': object_stats
    }

    return output


def main():
    input_data = json.load(sys.stdin)

    try:
        result = count_size_and_occurences(input_data)
    except RuntimeError as e:
        sys.stderr.write(str(e))
        sys.stderr.flush()
        sys.exit(0)
    else:
        json.dump(result, sys.stdout)

if __name__ == '__main__':
    main()
