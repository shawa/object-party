#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

readonly INFILE="$1"
readonly COUNTED_DOMAINS_DIR="counted-domains"
readonly FIRST_PARTY="$(jq --raw-output '.domain' < "$INFILE")"

true |
    openssl s_client -connect "$FIRST_PARTY:443" 2> /dev/null |
    openssl x509 -noout -text 2> /dev/null |
    grep 'DNS:' |
    sed -r 's/ ?DNS://g' |
    sed 's/^ *//' |
    tr -d '\n' |
    jq --raw-input --slurp --arg 'FIRST_PARTY' "$FIRST_PARTY"\
        '. |split(",") | { domain: $FIRST_PARTY, alts: .}'
