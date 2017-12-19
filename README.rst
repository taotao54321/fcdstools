=========
fcdstools
=========

`Famicom Disk System <https://en.wikipedia.org/wiki/Family_Computer_Disk_System>`_
disk image manipulation tools.

``fdscheck`` can recognize game titles with the internal database.
This database is converted from
`FDS Study database <http://www.geocities.jp/gponys/fmcmdskw11.html>`_,
and it is originally developed by
`ena <https://web.archive.org/web/20080515232015/http://fdsstudy.hp.infoseek.co.jp/>`_
and `gponys <http://www.geocities.jp/gponys/>`_. Thanks for the great
work and the permission to use!


Usage
=====

check::

    $ fdscheck game.fds                 # with internal database
    $ fdscheck --db fdsdb.json game.fds # with custom database
    $ fdscheck --nodb game.fds          # without database

split::

    $ fdssplit game.fds

build::

    $ fdscheck -f manifest game.fds > manifest.json
    $ fdssplit game.fds
    ... (modify files)
    $ fdsbuild out.fds manifest.json

convert FDS Study database into JSON::

    $ fdssjson fdsdb-be.txt > fdsdb.json

To convert Japanese database, encoding conversion is needed::

    $ iconv -f cp932 -t utf-8 fdsdb-bj.txt > fdsdb-bj-utf8.txt
    $ fdssjson fdsdb-bj-utf8.txt > fdsdb-ja.json


Install
=======

::

    $ pip install fcdstools


Dependency
==========

* Python >= 3.6
* `setuptools <https://pypi.python.org/pypi/setuptools>`_
* `kaitaistruct <https://pypi.python.org/pypi/kaitaistruct>`_
* `tabulate <https://pypi.python.org/pypi/tabulate>`_

To compile ``*.ksy`` files by yourself, HEAD of
`kaitai-struct-compiler <https://github.com/kaitai-io/kaitai_struct_compiler>`_
is required.


Resources
=========

* `nesdev wiki <https://wiki.nesdev.com/w/index.php/Family_Computer_Disk_System>`_
* `gponys' FDS resources <http://www.geocities.jp/gponys/fmcmdskw.html>`_
* `Enri's FDS page <http://www43.tok2.com/home/cmpslv/Famic/Famdis.htm>`_


Credits
=======

* `ena <https://web.archive.org/web/20080515232015/http://fdsstudy.hp.infoseek.co.jp/>`_
  developed `FDS Study <http://www.geocities.jp/gponys/fmcmdskw11.html>`_.
* `gponys <http://www.geocities.jp/gponys/>`_
  is maintaining
  `FDS Study unofficial database <http://www.geocities.jp/gponys/fmcmdskw11.html>`_.
