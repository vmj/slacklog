#!/bin/sh

#
#   Where to fetch the ChangeLogs from:
#
BASE_URL=http://ftp.osuosl.org/pub/slackware

#
#   Where to store the ChangeLogs once downloaded
#
BASE_DIR=./test/changelogs

#
#   Where to store the RSS feeds
#
RSS_DIR=./test/rss

#
#   Use one lastBuildDate for every feed for consistency
#
LAST_BUILD_DATE="$(date -Iseconds)"

#
#   A function that knows how to update a single feed.
#
update_rss() {
    slackware=$1
    version=$2
    min_date=$3

    echo -n "Generating RSS for $slackware $version... "

    #
    #   Update the RSS feed
    #
    LANG=en_US.utf8 slacklog2rss \
        --changelog "$BASE_DIR/$slackware-$version.txt" \
        --min-date="$min_date" \
        --out "$RSS_DIR/$slackware-$version.rss" \
        --slackware="$slackware $version" \
        --rssLink="http://linuxbox.fi/~vmj/slacklog/$slackware-$version.rss" \
        --description="Recent changes in $slackware $version" \
        --managingEditor="vmj@linuxbox.fi (Mikko Värri)" \
        --webMaster="vmj@linuxbox.fi (Mikko Värri)" \
        --lastBuildDate="$LAST_BUILD_DATE"

    echo "OK"
}

mkdir -p "$RSS_DIR"

#
#   Store the last build date for tests
#
echo "$LAST_BUILD_DATE" >"$RSS_DIR-timestamp"

#   Update various feeds.

#   For stable releases, the below date is the date of the first
#   patch to the -current branch.  I.e. the slackware 13.0 feed
#   would then contain all the changes made to the -current until
#   it became a release, and all the changes after that.
update_rss slackware   12.0    'Wed Oct 25 15:45:46 CDT 2006'
update_rss slackware   12.1    'Thu Jul 19 12:50:36 CDT 2007'
update_rss slackware   13.0    'Wed May  7 16:13:31 CDT 2008'
update_rss slackware64 13.0    'Tue May 19 15:36:49 CDT 2009'
update_rss slackware   13.1    'Mon Sep  7 20:58:42 CDT 2009'
update_rss slackware64 13.1    'Mon Sep  7 20:58:42 CDT 2009'
update_rss slackware   13.37   'Fri Jun 18 18:12:04 UTC 2010'
update_rss slackware64 13.37   'Fri Jun 18 18:12:04 UTC 2010'
update_rss slackware   14.0    'Wed Oct 10 03:06:03 UTC 2012'
update_rss slackware64 14.0    'Wed Oct 10 03:06:03 UTC 2012'
update_rss slackware   14.1    'Mon Nov 18 20:52:16 UTC 2013'
update_rss slackware64 14.1    'Mon Nov 18 20:52:16 UTC 2013'
update_rss slackware   14.2    'Tue Jul  5 04:52:45 UTC 2016'
update_rss slackware64 14.2    'Tue Jul  5 04:52:45 UTC 2016'

#   For current, use some very old date.
update_rss slackware   current 'Thu Jan  1 00:00:00 UTC 1970'
update_rss slackware64 current 'Thu Jan  1 00:00:00 UTC 1970'
