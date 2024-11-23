import socket
import argparse

def decode(data, key):
    key_bytes = key.encode()
    key_length = len(key_bytes)
    return bytes(data[i] ^ key_bytes[i % key_length] for i in range(len(data)))

def main():
    parser = argparse.ArgumentParser(
        prog='TorNet',
        description='Best torrent client!'
    )

    parser.add_argument('torrent', help="Path to the torrent file")
    args = parser.parse_args()

    with open(args.torrent, "r") as torrent_file:
        targs = [line.strip() for line in torrent_file]

    server_address = targs[0]
    server_port = int(targs[1])
    output_file = targs[2]
    key = targs[3]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Connecting to {server_address}:{server_port}...")
            s.connect((server_address, server_port))
            print("Connection established.")

            with open(output_file, "wb") as file:
                print(f"Receiving file: {output_file}")
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    file_data = decode(data, key)
                    file.write(file_data)

            print(f"File {output_file} downloaded successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
