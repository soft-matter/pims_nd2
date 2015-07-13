pims_nd2
========

This package lets [pims](https://github.com/soft-matter/pims) interface with the [ND2SDK](http://www.nd2sdk.com) for fast reading of Nikon *.nd2 files.
Currently, this is only implemented for windows and Python 2.7.

SDKs for Linux and OSX are already included, these are probably easy to implement.

Dependencies
------------

Apart from [pims](https://github.com/soft-matter/pims) there are no extra dependencies. The required c libraries are included and will be added to the PATH variable at runtime. 

Example
-------

The following code opens the demo file included in the package and displays the first 3D frame.

    from pims_nd2 import ND2_Reader
    frames = ND2_Reader('cluster.nd2')
	frames.bundle_axes = 'zyx'
	frames[0]
	
Supporting Grant
----------------
This reader was developed in part by Casper van der Wel, as part of his PhD thesis work in Daniela Kraft’s group at the Huygens-Kamerlingh-Onnes laboratory, Institute of Physics, Leiden University, The Netherlands. This work was supported by the Netherlands Organisation for Scientific Research (NWO/OCW).
