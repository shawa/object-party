#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

readonly COUNTED_DOMAINS_DIR="$1"
readonly OUTPUT_DIR="$2"

for file in $(find "$COUNTED_DOMAINS_DIR" -type f); do
    FIRST_PARTY="$(jq --raw-output '.domain' < "$file")"
    (./fetch-alt-names.sh "$file" | tee "$OUTPUT_DIR/$FIRST_PARTY.json") || >&2 echo "Couldn't fetch cert for $FIRST_PARTY"
done
