#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

readonly FIRST_PARTY="$1"

true |
    openssl s_client -connect "$FIRST_PARTY:443" 2> /dev/null | # retrieve cert
    openssl x509 -noout -text 2> /dev/null |                    # read cert to stdout
    grep 'DNS:' |                                               # find domain entries
    sed -r 's/ ?DNS://g' |                                      # filter to comma-separated domains
    sed 's/^ *//' |                                             # remove leading whitespace
    tr -d '\n' |                                                # remove traling newline
    jq --raw-input --slurp --arg 'FIRST_PARTY' "$FIRST_PARTY" \
        '. |split(",") | { domain: $FIRST_PARTY, alts: .}'
