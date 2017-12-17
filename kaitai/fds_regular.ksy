meta:
  title: 'Famicom Disk System disk image - regular format'
  id: fds_regular
  file-extension: fds
  imports:
    - fds_header
    - fds_info_block
    - fds_file_header_block
doc-ref: https://wiki.nesdev.com/w/index.php/Family_Computer_Disk_System

seq:
  - id: header
    type: fds_header
    size: 16
  - id: sides
    type: side
    size: 65500
    repeat: expr
    repeat-expr: header.side_count
types:
  side:
    seq:
      - id: info_block_code
        contents: [1]
      - id: info
        type: fds_info_block
      - id: amount_block_code
        contents: [2]
      - id: amount
        type: u1
      - id: files
        type: file
        repeat: expr
        repeat-expr: amount
  file:
    seq:
      - id: file_header_block_code
        contents: [3]
      - id: header
        type: fds_file_header_block
      - id: file_data_block_code
        contents: [4]
      - id: data
        size: header.size
