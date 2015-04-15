MediaMon
========

File monitor and auto-indexer for Synology DiskStation NAS.

I'm using this on a DS215j
It's a custom music-oriented version of the media indexer to work with BTSync folders.


Usage
-----

1. Install Python from the DiskStation package manager.

2. Edit mediamon.py ``watched_paths`` variable with the folders you want to keep indexed by synology-mediamon

3. Edit mediamon.py ``allowed_exts`` variable with the extensions you want to keep indexed by synology-mediamon

4. SSH into your DiskStation as root (e.g. ``ssh root@192.168.1.20`` -- use the
   right IP address for your DiskStation) and install pyinotify::

    cd /root/
    wget https://pypi.python.org/packages/source/p/pyinotify/pyinotify-0.9.5.tar.gz
    tar -xzvf pyinotify-0.9.5.tar.gz
    cd pyinotify-0.9.5/
    python setup.py install

5. Copy ``mediamon.py`` to the DiskStation's ``/root/`` directory (``scp
   mediamon.py root@192.168.1.20:/root/``).

6. Copy ``S99mediamon.sh`` to the DiskStation's ``/usr/syno/etc/rc.d/``
   directory (``scp S99mediamon.sh
   root@192.168.1.20:/usr/syno/etc/rc.d/``).

7. SSH into the DiskStation again and run ``chmod 755 /usr/syno/etc/rc.d/S99mediamon.sh``,
   then ``/usr/syno/etc/rc.d/S99mediamon.sh start`` to start up the monitor.

8. Add some media files to some folder you specified in the watched_paths variable, and check the log at 
   ``/var/log/mediamon.log`` to verify that it's working. You should see a ``synoindex -a`` entry for each 
   added file.


Caveats
-------

I've noticed I have to repeat steps 2-5 after any DSM upgrade. There may be a
way to avoid this by placing files in some other location that isn't wiped out
by DSM upgrades, but so far I haven't looked into it. I don't think
``S99mediamon.sh`` would work to restart the monitor after reboot if placed
anywhere else.

Suggestions, improvements, bug reports or pull requests welcome!


Credits
-------

Based on github.com/carljm/synology-mediamon
