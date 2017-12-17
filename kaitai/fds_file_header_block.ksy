meta:
  title: 'Famicom Disk System disk image - file header block'
  id: fds_file_header_block
doc-ref: https://wiki.nesdev.com/w/index.php/Family_Computer_Disk_System

seq:
  - id: seq_num
    type: u1
  - id: id
    type: u1
  - id: name
    size: 8
  - id: addr
    type: u2le
  - id: size
    type: u2le
  - id: type
    type: u1
