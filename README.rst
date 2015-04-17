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

5. Copy ``mediamon.py`` to the DiskStation's ``/usr/local/`` directory (``scp
   mediamon.py root@192.168.1.20:/usr/local/`` or use WinSCP).

6. Copy ``S99mediamon.sh`` to the DiskStation's ``/usr/local/etc/rc.d/``
   directory (``scp S99mediamon.sh root@192.168.1.20:/usr/local/etc/rc.d/`` or use WinSCP).

7. SSH into the DiskStation again and run ``chmod 755 /usr/local/etc/rc.d/S99mediamon.sh``,
   then ``/usr/local/etc/rc.d/S99mediamon.sh start`` to start up the monitor.

8. Add some music files to some folder you specified in the watched_paths variable, and check the log at 
   ``/var/log/mediamon.log`` to verify that it's working. You should see a ``synoindex -a`` entry for each 
   added file.

Credits
-------

Based on github.com/carljm/synology-mediamon
