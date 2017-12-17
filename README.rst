=========
fcdstools
=========

`Famicom Disk System <https://en.wikipedia.org/wiki/Family_Computer_Disk_System>`_
disk image manipulation tools.

``fdscheck`` supports
`FDS Study database <http://www.geocities.jp/gponys/fmcmdskw11.html>`_
by gponys. To use it, convert it into JSON with ``fdssjson``.

I wanted to name this "fdstools", but it had been already
`taken <https://pypi.python.org/pypi/fdstools/>`_.


Usage
=====

check::

    $ fdscheck game.fds                 # without DB
    $ fdscheck --db fdsdb.json game.fds # with DB

split::

    $ fdssplit game.fds

build::

    $ fdscheck -f manifest game.fds > manifest.json
    $ fdssplit game.fds
    ... (modify files)
    $ fdsbuild out.fds manifest.json

convert FDS Study database into JSON::

    $ fdssjson fdsdb-be.txt > fdsdb.json


Install
=======

::

    $ pip install .


Dependency
==========

* `kaitaistruct <https://pypi.python.org/pypi/kaitaistruct>`_
* `tabulate <https://pypi.python.org/pypi/tabulate>`_

To compile ``*.ksy`` files by yourself, HEAD of
`kaitai-struct-compiler <https://github.com/kaitai-io/kaitai_struct_compiler>`_
is required.


Resources
=========

* `nesdev wiki <https://wiki.nesdev.com/w/index.php/Family_Computer_Disk_System>`_
* `gponys' FDS resources <http://www.geocities.jp/gponys/fmcmdskw.html>`_


