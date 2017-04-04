#!/bin/sh

#
#   Where to fetch the ChangeLogs from:
#
BASE_URL=http://ftp.osuosl.org/pub/slackware

#
#   Where to store the ChangeLogs once downloaded
#
BASE_DIR=.

#
#   Temporary storage
#
TMP_DIR=/tmp

#
#   A function that knows how to update a single feed.
#
update_rss() {
    slackware=$1
    version=$2
    min_date=$3

    #
    #   Download the ChangeLog.txt to temporary location.
    #   Use conditional GET and compression to minimize the
    #   download.
    #
    curl -sS -q --compressed \
        -z $BASE_DIR/$slackware-$version.txt \
        -R -o $TMP_DIR/$slackware-$version.txt \
        $BASE_URL/$slackware-$version/ChangeLog.txt

    #
    #   The ChangeLog.txt exists only if it had actually changed.
    #
    if [ -f $TMP_DIR/$slackware-$version.txt ] ; then
        #
        #   Move the ChangeLog.txt to real location
        #
        mv $TMP_DIR/$slackware-$version.txt $BASE_DIR/$slackware-$version.txt
        #
        #   Update the RSS feed
        #
        LANG=en_US.utf8 slacklog2rss \
            --changelog $BASE_DIR/$slackware-$version.txt \
            --min-date="$min_date" \
            --out $BASE_DIR/$slackware-$version.rss \
            --slackware="$slackware $version" \
            --rssLink="http://linuxbox.fi/~vmj/slacklog/$slackware-$version.rss" \
            --description="Recent changes in $slackware $version" \
            --managingEditor="vmj@linuxbox.fi (Mikko Värri)" \
            --webMaster="vmj@linuxbox.fi (Mikko Värri)"
    fi
}


#   Update various feeds.

#   For stable releases, the date is the date of the first patch,
#   since the next entry would be the announcement of the previous
#   release.
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
