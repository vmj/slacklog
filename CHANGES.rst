Release history
===============


Version 0.9.4 (2017-09-03)
--------------------------

The parser subclass can now overwrite the generation of entry identifier and/or checksum.

Other than that, tests were updated to use python-dateutil 2.6.1, and documentation was fixed.


Version 0.9.3 (2017-08-23)
--------------------------

This release is mainly bug fixing.  RSS and atom formatters learnt to take
the feed build time (optionally) as an argument, which makes them more testable.


Version 0.9.2 (2017-05-25)
--------------------------

This release is backwards incompatible with the previous releases:
SlackLogParser and SlackLogFormatter (and subclasses) have to be instantiated,
and instead of using class methods, instance methods and properties have to be used.


Version 0.9.1 (2017-05-24)
--------------------------

This release adds checksum, identifier, and parent fields to SlackLogEntry.
Also, a couple of bugs with recognizing package names was resolved.


Verions 0.9.0 (2017-04-05)
--------------------------

After almost six years with only maintenance releases, it's time to move to beta.

This release switches from distutils to setuptools, and contains some refactoring to scripts (pure refactoring, no
changes in the CLI).


Version 0.0.9 (2017-04-04)
--------------------------

This release does not add any new functionality.

The dependencies were updated: Python 2.7, 3.3 - 3.6, and python-dateutil 2.1 - 2.6.
Support for Python 2.6 was dropped, not because it doesn't work but because Python core team doesn't support it.

The code was formatted according to PEP-8, and the example script was updated to include Slackware versions 14.0 and
14.2.


Version 0.0.8 (2014-09-28)
--------------------------

This release does not add any new functionality, but includes support
for Python 3.

In addition, Slackware{,64} 14.1 was added to the example script, and
Travis CI and ReadTheDocs were integrated (see the links at the top of
the README).

Version 0.0.7 (2011-06-16)
--------------------------

This release adds Atom feed formatter, and fixes compatibility issue
with recent ChangeLog.txt format change which caused empty entries to
be generated.  Also, Slackware{,64} 13.37 was added to the example
script.


Version 0.0.6 (2011-03-18)
--------------------------

This release adds documentation.


Version 0.0.5 (2011-03-17)
--------------------------

This release adds the example script in source distribution, too.


Version 0.0.4 (2011-03-17)
--------------------------

This release contains better error handling, better compatibility with
more feed readers, better support for timezones other that UTC, and an
example script suitable for a cron job to update RSS feeds.


Version 0.0.3 (2011-02-21)
--------------------------

Added PyBlosxom formatter and fixed a couple of issues.


Version 0.0.2 (2011-01-29)
--------------------------

Packaging cleanups.


Version 0.0.1 (2011-01-28)
--------------------------

Initial release.
