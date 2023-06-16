#!/usr/bin/env bash
# backs up all files in the current directory to a temporary folder

TEMP_DIR="temp_backup"
ITEMS=$(ls)

this="$(basename "$0")"
mkdir -p "$TEMP_DIR";
for ITEM in $ITEMS; do
    if [ "$ITEM" != "$TEMP_DIR" ] && [ "$ITEM" != "$this" ] && [ "$ITEM" != "restore.sh" ]; then
	cp "$ITEM" "$TEMP_DIR"/"$ITEM";
	echo "Copied $ITEM  ->  $ITEM";
    fi
done
