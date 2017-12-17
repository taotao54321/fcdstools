# -*- coding: utf-8 -*-

import struct

from kaitaistruct import KaitaiStream, BytesIO

from . import util

from .kaitai.fds_header            import FdsHeader          as _ksFdsHeader
from .kaitai.fds_info_block        import FdsInfoBlock       as _ksFdsInfoBlock
from .kaitai.fds_file_header_block import FdsFileHeaderBlock as _ksFdsFileHeaderBlock

# imitation struct {{{
class Fds:
    def __init__(self, sides):
        self.sides  = sides

class FdsHeader:
    def __init__(self, side_count):
        self.magic      = _FDS_MAGIC
        self.side_count = side_count

class FdsSide:
    def __init__(self, info, amount, files):
        self.info_block_code   = _FDS_INFO_BLOCK_CODE
        self.info              = info
        self.amount_block_code = _FDS_AMOUNT_BLOCK_CODE
        self.amount            = amount
        self.files             = files

class FdsInfo:
    def __init__(
        self, *,
        verification,
        maker,
        game_id,
        version,
        side_id,
        disk_id,
        disk_type,
        unknown1,
        boot_file,
        unknown2,
        date,
        country,
        unknown3,
        unknown4,
        unknown5,
        unknown6,
        rewrite_date,
        unknown7,
        unknown8,
        writer_serial,
        unknown9,
        rewrite_count,
        side_id_actual,
        unknown10,
        version_debug,
    ):
        _chk_len(verification,  14, "verification")
        _chk_len(game_id,        4, "game_id")
        _chk_len(unknown2,       5, "unknown2")
        _chk_len(date,           3, "date")
        _chk_len(unknown5,       2, "unknown5")
        _chk_len(unknown6,       5, "unknown6")
        _chk_len(rewrite_date,   3, "rewrite_date")
        _chk_len(writer_serial,  2, "writer_serial")

        self.verification   = verification
        self.maker          = maker
        self.game_id        = game_id
        self.version        = version
        self.side_id        = side_id
        self.disk_id        = disk_id
        self.disk_type      = disk_type
        self.unknown1       = unknown1
        self.boot_file      = boot_file
        self.unknown2       = unknown2
        self.date           = date
        self.country        = country
        self.unknown3       = unknown3
        self.unknown4       = unknown4
        self.unknown5       = unknown5
        self.unknown6       = unknown6
        self.rewrite_date   = rewrite_date
        self.unknown7       = unknown7
        self.unknown8       = unknown8
        self.writer_serial  = writer_serial
        self.unknown9       = unknown9
        self.rewrite_count  = rewrite_count
        self.side_id_actual = side_id_actual
        self.unknown10      = unknown10
        self.version_debug  = version_debug

class FdsFile:
    def __init__(self, header, data):
        self.file_header_block_code = _FDS_FILE_HEADER_BLOCK_CODE
        self.header                 = header
        self.file_data_block_code   = _FDS_FILE_DATA_BLOCK_CODE
        self.data                   = data

class FdsFileHeader:
    def __init__(self, *, seq_num, id, name, addr, size, type):
        _chk_len(name, 8, "name")

        self.seq_num = seq_num
        self.id      = id
        self.name    = name
        self.addr    = addr
        self.size    = size
        self.type    = type
# }}}

class LoadError(Exception): pass

class SaveError(Exception): pass

def load(in_):
    """load FDS, not trusting file counts in amount blocks."""
    buf = in_.read()

    side_count, r = divmod(len(buf), _FDS_SIDE_SIZE)
    if side_count == 0:
        raise LoadError("incomplete file")
    if r not in (0,16):
        raise LoadError(f"file size must be (0 or 16) + {_FDS_SIDE_SIZE}*n (n >= 1)")

    in_ = _stream(buf)

    try:
        header = None
        if r == 16:
            header = _ksFdsHeader(_stream(in_.read_bytes(_FDS_HEADER_SIZE)))
            # ignore header.side_count

        sides  = []
        for _ in range(side_count):
            side = _parse_side(_stream(in_.read_bytes(_FDS_SIDE_SIZE)))
            sides.append(side)
        return header, Fds(sides)
    except LoadError:
        raise
    except Exception as e:
        raise LoadError(f"{e}") from e

def save(out, header, disk):
    """save FDS."""
    if header:
        buf = struct.pack("< 4s B", header.magic, header.side_count)
        buf = util.nulpad(buf, _FDS_HEADER_SIZE)
        out.write(buf)

    for i, side in enumerate(disk.sides):
        buf = _pack_side(side)
        # TODO: this is not a true disk capacity
        #       (https://wiki.nesdev.com/w/index.php/Family_Computer_Disk_System#Data_not_stored_in_the_FDS_image)
        if len(buf) > _FDS_SIDE_SIZE:
            raise SaveError(f"side #{i} is too big")
        buf = util.nulpad(buf, _FDS_SIDE_SIZE)
        out.write(buf)

def is_valid_game_id(o):
    if isinstance(o, str) and len(o) == 4:
        return all(is_valid_game_id_byte(ord(c)) for c in o)
    elif isinstance(o, bytes) and len(o) == 4:
        return all(is_valid_game_id_byte(b) for b in o)
    return False

def is_valid_game_id_byte(b: int):
    return util.is_ascii_nonctl(b)

def sanitize_filename(name: bytes, si, fi):
    """sanitize filename of a file.

    name -- name on disk image
    si   -- side index             (0-based)
    fi   -- file index in the side (0-based, not a sequence number)
    """
    name = name.rstrip(b"\x00")
    if util.is_ascii_nonctl(name):
        fname = "".join(map(
            lambda c: c if util.is_filename_safe(c) else "_",
            name.decode("ascii")
        ))
    else:
        fname = "FILE"

    # some games have duplicate names, so add file index
    return f"{si}-{fi:02d}-{fname}"

_FDS_MAGIC = b"FDS\x1a"

_FDS_HEADER_SIZE            =    16
_FDS_SIDE_SIZE              = 65500
_FDS_INFO_BLOCK_SIZE        =    55 # without block code
_FDS_FILE_HEADER_BLOCK_SIZE =    15 # without block code

_FDS_INFO_BLOCK_CODE        = 1
_FDS_AMOUNT_BLOCK_CODE      = 2
_FDS_FILE_HEADER_BLOCK_CODE = 3
_FDS_FILE_DATA_BLOCK_CODE   = 4

# loading {{{
def _parse_side(in_):
    if in_.read_u1() != _FDS_INFO_BLOCK_CODE:
        raise LoadError("info block code not found")
    info = _ksFdsInfoBlock(_stream(in_.read_bytes(_FDS_INFO_BLOCK_SIZE)))

    if in_.read_u1() != _FDS_AMOUNT_BLOCK_CODE:
        raise LoadError("amount block code not found")
    amount = in_.read_u1()

    files = list(_parse_files(in_))

    return FdsSide(info, amount, files)

def _parse_files(in_):
    """parse files greedily."""
    while True:
        try:
            if in_.read_u1() != _FDS_FILE_HEADER_BLOCK_CODE:
                return
            header = _ksFdsFileHeaderBlock(
                _stream(in_.read_bytes(_FDS_FILE_HEADER_BLOCK_SIZE)))
            if in_.read_u1() != _FDS_FILE_DATA_BLOCK_CODE:
                return
            data = in_.read_bytes(header.size)
        except Exception:
            return
        yield FdsFile(header, data)

def _stream(buf):
    return KaitaiStream(BytesIO(buf))
# }}}

# saving {{{
def _pack_side(side):
    res = bytearray()

    # info block
    info = side.info
    res += b"\x01"
    res += struct.pack("< 14s", info.verification)
    res += struct.pack("< B",   info.maker)
    res += struct.pack("< 4s",  info.game_id)
    res += struct.pack("< B",   info.version)
    res += struct.pack("< B",   info.side_id)
    res += struct.pack("< B",   info.disk_id)
    res += struct.pack("< B",   info.disk_type)
    res += struct.pack("< B",   info.unknown1)
    res += struct.pack("< B",   info.boot_file)
    res += struct.pack("< 5s",  info.unknown2)
    res += struct.pack("< 3s",  info.date)
    res += struct.pack("< B",   info.country)
    res += struct.pack("< B",   info.unknown3)
    res += struct.pack("< B",   info.unknown4)
    res += struct.pack("< 2s",  info.unknown5)
    res += struct.pack("< 5s",  info.unknown6)
    res += struct.pack("< 3s",  info.rewrite_date)
    res += struct.pack("< B",   info.unknown7)
    res += struct.pack("< B",   info.unknown8)
    res += struct.pack("< 2s",  info.writer_serial)
    res += struct.pack("< B",   info.unknown9)
    res += struct.pack("< B",   info.rewrite_count)
    res += struct.pack("< B",   info.side_id_actual)
    res += struct.pack("< B",   info.unknown10)
    res += struct.pack("< B",   info.version_debug)

    # amount block
    res += b"\x02"
    res += struct.pack("< B", side.amount)

    for f in side.files:
        # file header block
        h = f.header
        res += b"\x03"
        res += struct.pack("< B",  h.seq_num)
        res += struct.pack("< B",  h.id)
        res += struct.pack("< 8s", h.name)
        res += struct.pack("< H",  h.addr)
        res += struct.pack("< H",  h.size)
        res += struct.pack("< B",  h.type)

        # file data block
        res += b"\x04"
        res += f.data

    return bytes(res)
# }}}

def _chk_len(seq, n, name):
    if len(seq) != n:
        raise ValueError(f"length of {name} must be {n}: {seq}")
