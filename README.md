# TorNet
Simple async low-level data transfer in Python, that use encryption.

## Torrent file

This is structure of torrent file:
<code lang="text">127.0.0.1  # IP-address to connect/bind
  8080       # Port to connect/bind
  img.jpg    # File to transfer
  key        # Encryption key</code>

## How to run?

First of all, you need to fill out a torrent file.
Than run a server and clients will able to connect and download your file.
Note: torrent-file must be same on server and client devices.
