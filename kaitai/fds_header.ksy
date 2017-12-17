meta:
  title: 'Famicom Disk System disk image - header'
  id: fds_header
doc-ref: https://wiki.nesdev.com/w/index.php/Family_Computer_Disk_System

seq:
  - id: magic
    contents: [0x46, 0x44, 0x53, 0x1A]
  - id: side_count
    type: u1
  - id: reserved
    size-eos: true
