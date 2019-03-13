#!/usr/bin/env bash

#
#   Where to fetch the ChangeLogs from:
#
BASE_URL=http://ftp.osuosl.org/pub/slackware

#
#   Where to store the ChangeLogs once downloaded
#
DST_DIR=./test/changelogs

#
#   Temporary storage
#
TMP_DIR="$(mktemp -d)"

#
#   A function that knows how to download one ChangeLog
#
fetch_changelog() {
    slackware=$1
    version=$2

    echo -n "Fetching ChangeLog.txt for $slackware $version... "
    #
    #   Download the ChangeLog.txt to temporary location.
    #   Use conditional GET and compression to minimize the
    #   download.
    #
    curl -sS -q --compressed \
        -z "$DST_DIR/$slackware-$version.txt" \
        -R -o "$TMP_DIR/$slackware-$version.txt" \
        "$BASE_URL/$slackware-$version/ChangeLog.txt"

    #
    #   The tmp ChangeLog.txt exists only if it had actually changed.
    #
    if [ -f "$TMP_DIR/$slackware-$version.txt" ] ; then
        #
        #   Move the ChangeLog.txt to real location
        #
        mv "$TMP_DIR/$slackware-$version.txt" \
           "$DST_DIR/$slackware-$version.txt"
        echo "OK"
    else
        echo "UP-TO-DATE"
    fi
}

cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT
mkdir -p "$DST_DIR"


fetch_changelog slackware   12.0
fetch_changelog slackware   12.1
fetch_changelog slackware   13.0
fetch_changelog slackware64 13.0
fetch_changelog slackware   13.1
fetch_changelog slackware64 13.1
fetch_changelog slackware   13.37
fetch_changelog slackware64 13.37
fetch_changelog slackware   14.0
fetch_changelog slackware64 14.0
fetch_changelog slackware   14.1
fetch_changelog slackware64 14.1
fetch_changelog slackware   14.2
fetch_changelog slackware64 14.2
fetch_changelog slackware   current
fetch_changelog slackware64 current
