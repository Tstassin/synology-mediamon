MediaMon
========

Music folders monitor and auto-indexer for Synology DiskStation NAS.
Credit and inspiration to github.com/carljm

I'm using this on a DS215j.
It's a custom music-oriented version of the media indexer to work with BTSync or Syncthing folders.
It works as a daemon, install it and it's done.
It works (normally) across DSM Updates.

Files
-----

- README.rst : This readme
- mediamon.cfg : Personal user settings
- mediamon.py : Media monitor "engine"
- S99mediamon.sh : Media monitor daemon start/stop

Usage - First Installation
--------------------------

#. To start monitoring with your existing files correctly indexed, update the index of your library (DSM -> Control Panel -> Indexing Service > Re-Index). This operation might take up to a few hours. After indexing is done, goto "Indexed folders list" and disable the folders you'll want synology-mediamon to take care of.

#. Install Python3 from the DiskStation package manager.

#. From the DSM, go to your user home directory and download synology-mediamon files.

#. Edit ``mediamon.cfg`` file to specify the folders you want to keep indexed, the extensions to index and subfolders to exclude from indexed folders.

#. SSH into your DiskStation with your admin login and password 

#. Install pyinotify for Python 3 : ``python3 -m ensurepip`` and ``/volume1/\@appstore/py3k/usr/local/bin/pip3 install pyinotify``


#. Install configparser module ``pip install configparser``


#. Navigate to your user home directory where you downloaded the files (e.g. ``/volume1/homes/thomas/synology-mediamon``)


#. Create a directory ``mkdir /usr/local/mediamon`` and copy the two files mediamon.py and mediamon.cfg with chmod 755 ``cp mediamon.* /usr/local/mediamon/ && chmod -R 755 /usr/local/mediamon/``

#. Copy S99mediamon.sh to his place ``cp S99mediamon.sh /usr/local/etc/rc.d && chmod 755 /usr/local/etc/rc.d/S99mediamon.sh``

#. Run ``/usr/local/etc/rc.d/S99mediamon.sh start`` to start up the monitor.

7. Add some music files to some folder you specified in the config file, and check the log at
   ``/var/log/mediamon.log`` to verify that it's working. You should see a ``synoindex -a`` entry for each added file.

Updating
--------

1. Overwrite old ``mediamon.py`` to the DiskStation's ``/usr/local/`` directory.

2. Restart Disktation
   OR
   Type ``/usr/local/etc/rc.d/S99mediamon.sh stop`` then  ``/usr/local/etc/rc.d/S99mediamon.sh start``
   to restart the monitor.

Credits
-------
github.com/tstassin
Based on github.com/carljm/synology-mediamon
