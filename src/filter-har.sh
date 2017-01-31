#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

readonly INFILE="$1"

domain() {
    perl -ne '/https?:\/\/(.+?)\// and print "$1\n"'
}

readonly FIRST_PARTY="$(jq '.log.entries[0].request.url' < "$INFILE" | domain)"

cat "$INFILE" |
    jq --arg FIRST_PARTY "$FIRST_PARTY" '.log.entries
        | map ({url: (.request.url| match("https?://(.+?)/"; "g").captures[0].string),
                bytes: .response.content.size} )
        | {domain: $FIRST_PARTY, objects: .}' |
    python3 ./count-origin-stats.py
