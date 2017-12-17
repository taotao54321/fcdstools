# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
import struct


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class FdsInfoBlock(KaitaiStruct):
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
        self.verification = self._io.ensure_fixed_contents(struct.pack('14b', 42, 78, 73, 78, 84, 69, 78, 68, 79, 45, 72, 86, 67, 42))
        self.maker = self._io.read_u1()
        self.game_id = self._io.read_bytes(4)
        self.version = self._io.read_u1()
        self.side_id = self._io.read_u1()
        self.disk_id = self._io.read_u1()
        self.disk_type = self._io.read_u1()
        self.unknown1 = self._io.read_u1()
        self.boot_file = self._io.read_u1()
        self.unknown2 = self._io.read_bytes(5)
        self.date = self._io.read_bytes(3)
        self.country = self._io.read_u1()
        self.unknown3 = self._io.read_u1()
        self.unknown4 = self._io.read_u1()
        self.unknown5 = self._io.read_bytes(2)
        self.unknown6 = self._io.read_bytes(5)
        self.rewrite_date = self._io.read_bytes(3)
        self.unknown7 = self._io.read_u1()
        self.unknown8 = self._io.read_u1()
        self.writer_serial = self._io.read_bytes(2)
        self.unknown9 = self._io.read_u1()
        self.rewrite_count = self._io.read_u1()
        self.side_id_actual = self._io.read_u1()
        self.unknown10 = self._io.read_u1()
        self.version_debug = self._io.read_u1()


