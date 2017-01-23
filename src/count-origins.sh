#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

readonly INFILE="$1"

domain() {
    perl -ne '/https?:\/\/(.+?)\// and print "$1\n"'
}

readonly FIRST_PARTY="$(jq '.log.entries[0].request.url' < "$INFILE" | domain)"

cat "$INFILE" |
    jq '.log.entries[].request.url' | # pull out request urls
    domain |                          # from this, grab the domain
    sort |                            # alphabetic sort, needed by uniq
    uniq --count |                    # count occurences of each domain
    sort --reverse --numeric-sort |   # sort in descending order by occurence
    sed -e 's/^ *//' |                # strip out the leading whitespace
    jq --raw-input --slurp --arg 'FIRST_PARTY' "$FIRST_PARTY" \
        '. | split("\n") | map(select(. != "")) | map (split(" ") | {domain: .[1], count: (.[0] | fromjson )}) | { domain: "\($FIRST_PARTY)", object_domains: .}'

