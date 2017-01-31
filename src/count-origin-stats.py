import subprocess
import sys
import json
from collections import defaultdict


def alternative_names(domain):
    '''
    for a given domain, return a set of all alternative names in its x509 cert
    '''
    alts = json.loads(subprocess.check_output(['./domain-alts.sh', domain]))
    return frozenset(alts["alts"])


def matches(cert_domain, domain):
    '''
    match a domain against the one listed in the x509 cert
    '''
    # first check they're the same, then otherwise if it's a wildcard match
    # i.e. www.google.com matches *.google.com
    return (cert_domain == domain or
            cert_domain.split('.') == ['*'] + domain.split('.')[1:])


def is_under_cert(cert_domains, domain):
    return any((matches(cert_domain, domain)
                for cert_domain in cert_domains))


def count_size_and_occurences(filtered_har):
    first_party_name = filtered_har['domain']
    alts = alternative_names(first_party_name)

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
        'is_first_party': is_under_cert(alts, domain),
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
    result = count_size_and_occurences(input_data)
    json.dump(result, sys.stdout)

if __name__ == '__main__':
    main()
