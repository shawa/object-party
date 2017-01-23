#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

readonly FILTER_COMMAND="$1"
readonly RAW_HARS_DIR="$2"
readonly COUNTED_DOMAINS_DIR="$3"

for file in $(find "$RAW_HARS_DIR" -type f); do
    outfile="$(basename "$file")"
    "$FILTER_COMMAND" "$file" |
        tee "$COUNTED_DOMAINS_DIR/$outfile.json"
    echo $file
done
