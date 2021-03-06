# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class FdsFileHeaderBlock(KaitaiStruct):
    """
    .. seealso::
       Source - https://wiki.nesdev.com/w/index.php/Family_Computer_Disk_System
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.seq_num = self._io.read_u1()
        self.id = self._io.read_u1()
        self.name = self._io.read_bytes(8)
        self.addr = self._io.read_u2le()
        self.size = self._io.read_u2le()
        self.type = self._io.read_u1()


