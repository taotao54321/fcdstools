# -*- coding: utf-8 -*-

"""FDS Study Database (Type-B)

Ref: http://www.geocities.jp/gponys/fmcmdskw11.html
"""

import itertools
import re

from . import fds
from . import util

class ParseError(Exception):
    def __init__(self, lineno, msg):
        s = f"line {lineno}: {msg}" if lineno > 0 else msg
        super().__init__(s)

def parse(in_):
    records = []

    for key, games in _parse_entries(in_):
        for title, sides in games:
            records.append(dict(
                key   = key,
                title = title,
                sides = sides,
            ))

    return dict(
        records = records,
    )

def match(db, disk):
    """search the best DB record matching with a disk.

    return (record, matches).
    if no entry is found, return (None, None).
    """
    KEY_UNL = "-UNL"

    # game id must be unique in a disk
    ids = set(side.info.game_id for side in disk.sides)
    if len(ids) != 1: return None, None

    # assume "strange" game id as unlicensed.
    game_id = ids.pop()
    key = game_id.decode("ascii") if fds.is_valid_game_id(game_id) else KEY_UNL

    sample = []
    for side in disk.sides:
        crcs = [util.crc32digest(f.data) for f in side.files]
        sample.append(crcs)

    score_best   = 0
    record_best  = None
    matches_best = None
    for record in db["records"]:
        if key != record["key"]: continue
        matches = _match_matrix(sample, record["sides"])
        if matches is None: continue
        score = sum(sum(row) for row in matches)
        if score_best < score:
            score_best   = score
            record_best  = record
            matches_best = matches

    return record_best, matches_best

_RE_MAGIC        = re.compile(r"\AFDS\s+Study\s+Database\s+Type-B")
_RE_CRC32_DIGEST = re.compile(r"\A[0-9a-f]{8}\Z")

def _parse_entries(in_):
    reader = _LineReader(in_)

    while True:
        line, lineno = reader.readline()
        if line is None: break
        if lineno == 1 and _RE_MAGIC.match(line): continue

        key, counts = _parse_id_line(line, lineno)

        games = tuple(_parse_games(reader, counts))
        if not games:
            raise ParseError(reader.lineno, "no game")

        yield key, games

def _parse_id_line(line, lineno):
    fields = line.split(",")
    assert fields
    if fields[0] == "@":
        fields.pop(0)
    if len(fields) < 2:
        raise ParseError(lineno, f"insufficient columns: '{line}'")

    # ignore trailing whitespaces
    key = fields[0][:4] + fields[0][4:].strip()
    if len(key) != 4:
        raise ParseError(lineno, f"length of game id must be 4: {key}")
    if not fds.is_valid_game_id(key):
        raise ParseError(lineno, f"illegal character in game id: {key}")

    try:
        counts = tuple(map(int, fields[1:]))
    except ValueError as e:
        raise ParseError(lineno, f"conversion to int failed: {e}")
    # permit 0 file on a side
    if any(cnt < 0 for cnt in counts):
        raise ParseError(lineno, f"file counts must be non-negative: '{line}'")

    return key, counts

def _parse_games(reader, counts):
    while True:
        line, lineno = reader.readline()
        if line is None: break
        reader.unreadline(line)
        if not line.startswith("\t"): break

        title = None
        sides = []
        for i in range(len(counts)):
            line, lineno = reader.readline()
            if line is None:
                raise ParseError(-1, "premature end of file")

            crcs, s = _parse_side(line, lineno, counts, i)
            sides.append(crcs)
            if i == len(counts)-1:
                title = s.strip()
                if not title:
                    raise ParseError(lineno, "game title is empty")

        yield title, sides

def _parse_side(line, lineno, counts, idx):
    if not line.startswith("\t"):
        raise ParseError(lineno, "disk-side line must start with tab")
    line = line.strip()

    cnt = counts[idx]
    fields = line.split(",", maxsplit=cnt+1) # sometimes game title contains ","
    if len(fields) != cnt+2:
        raise ParseError(lineno, f"column count must be {cnt+2}")

    try:
        counts_len = int(fields[0])
    except ValueError as e:
        raise ParseError(lineno, f"conversion to int failed: {e}")
    if counts_len != len(counts):
        raise ParseError(lineno, "disk-side count mismatch")

    crcs = tuple(map(str.lower, fields[1:-1]))
    if any(not _RE_CRC32_DIGEST.fullmatch(s) for s in crcs):
        raise ParseError(lineno, "not crc32 digest")

    return crcs, fields[-1]

class _LineReader:
    def __init__(self, in_):
        self._in     = in_
        self.lineno  = 0
        self._pushed = None
    def readline(self):
        """return (line, lineno).

        empty lines (containing only whitespaces) are skipped.
        newlines are stripped.
        lineno is 1-based.

        On EOF, return (None, None).
        """
        while True:
            line = self._nextline()
            if line is None: return None, None
            if not line.strip(): continue
            break
        return line.rstrip("\r\n"), self.lineno
    def unreadline(self, line):
        assert self._pushed is None
        self.lineno  -= 1
        self._pushed  = line
    def _nextline(self):
        if self._pushed is not None:
            line = self._pushed
            self._pushed = None
        else:
            line = self._in.readline()
            if not line: return None
        self.lineno += 1
        return line

def _match_matrix(sample, db_sides):
    # side count must be equal
    if len(sample) != len(db_sides): return None

    res = []
    for ss, ds in zip(sample, db_sides):
        n, m = len(ss), len(ds)
        if n < m: return None # sample has too few files
        res.append([s == d for s,d in itertools.zip_longest(ss,ds)])

    return res
