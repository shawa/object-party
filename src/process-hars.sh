#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

readonly FILTER_COMMAND="$1"
readonly INPUT_DIR="$2"
readonly OUTPUT_DIR="$3"

for file in $(find "$INPUT_DIR" -type f); do
    outfile="$(basename "$file")"
    echo "$file"
    "$FILTER_COMMAND" "$file" |
        tee "$OUTPUT_DIR/$outfile.json" |
        jq -r '.domain'
done
