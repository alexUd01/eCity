#!/usr/bin/env bash
# restore one or all backed-up all files from the temporary backup folder

TEMP_DIR="temp_backup"
ITEMS=$(ls "$TEMP_DIR"/)

this="$(basename "$0")"
for ITEM in $ITEMS; do
    if [ "$ITEM" != "$TEMP_DIR" ] && [ "$ITEM" != "$this" ] && [ "$ITEM" != "backup.sh" ]; then
	if cp "$TEMP_DIR"/"$ITEM" "$(pwd)"; then
	    echo "Copied $TEMP_DIR/$ITEM  ->  $ITEM";
	else
	    echo "Failed to copy $ITEM  ->  $(pwd)/";
	fi
    fi
done
