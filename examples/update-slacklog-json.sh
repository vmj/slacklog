#!/usr/bin/env bash

#
#   Where are the ChangeLogs stored
#
SRC_DIR=./test/changelogs

#
#   Where to store the JSON files
#
DST_DIR=./test/json

#
#   A function that knows how to update a single file.
#
update_json() {
    slackware=$1
    version=$2

    echo -n "Generating JSON for $slackware $version... "

    #
    #   Update the JSON file
    #
    LANG=C.UTF-8 slacklog2json \
        --changelog "$SRC_DIR/$slackware-$version.txt" \
        --out "$DST_DIR/$slackware-$version.json" \
        --indent 4

    echo "OK"
}

mkdir -p "$DST_DIR"

#   Update various files.

update_json slackware   12.0
update_json slackware   12.1
update_json slackware   13.0
update_json slackware64 13.0
update_json slackware   13.1
update_json slackware64 13.1
update_json slackware   13.37
update_json slackware64 13.37
update_json slackware   14.0
update_json slackware64 14.0
update_json slackware   14.1
update_json slackware64 14.1
update_json slackware   14.2
update_json slackware64 14.2
update_json slackware   current
update_json slackware64 current
