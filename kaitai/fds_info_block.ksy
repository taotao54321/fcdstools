meta:
  title: 'Famicom Disk System disk image - info block'
  id: fds_info_block
doc-ref: https://wiki.nesdev.com/w/index.php/Family_Computer_Disk_System

seq:
  - id: verification
    contents: [
      0x2A, 0x4E, 0x49, 0x4E, 0x54, 0x45, 0x4E,
      0x44, 0x4F, 0x2D, 0x48, 0x56, 0x43, 0x2A,
    ]
  - id: maker
    type: u1
  - id: game_id
    size: 4
  - id: version
    type: u1
  - id: side_id
    type: u1
  - id: disk_id
    type: u1
  - id: disk_type
    type: u1
  - id: unknown1
    type: u1
  - id: boot_file
    type: u1
  - id: unknown2
    size: 5
  - id: date
    size: 3
  - id: country
    type: u1
  - id: unknown3
    type: u1
  - id: unknown4
    type: u1
  - id: unknown5
    size: 2
  - id: unknown6
    size: 5
  - id: rewrite_date
    size: 3
  - id: unknown7
    type: u1
  - id: unknown8
    type: u1
  - id: writer_serial
    size: 2
  - id: unknown9
    type: u1
  - id: rewrite_count
    type: u1
  - id: side_id_actual
    type: u1
  - id: unknown10
    type: u1
  - id: version_debug
    type: u1
  # 16-bit CRC is omitted
