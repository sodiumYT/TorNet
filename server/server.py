import os
import argparse
import asyncio

class Server:
    def __init__(self):
        self.downloads = 0
        self.targs = []
        self.clients = []

    def encode(self, data):
        key = self.targs[3]
        key_bytes = key.encode()
        key_length = len(key_bytes)
        return bytes(data[i] ^ key_bytes[i % key_length] for i in range(len(data)))


    async def start(self, torrent):
        with open(torrent, "r") as torrent_file:
            self.targs = [line.strip() for line in torrent_file]

        self.server = await asyncio.start_server(
            self.handle_client, self.targs[0], int(self.targs[1])
        )
        print(f"Server started on {self.targs[0]}:{self.targs[1]}")
        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, reader, writer):
        self.clients.append(writer)
        self.update_title()

        try:
            file_path = self.targs[2]
            with open(file_path, "rb") as file:
                while chunk := file.read(4096):
                    writer.write(self.encode(chunk))
                    await writer.drain()

            print(f"File {file_path} sent to client.")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.clients.remove(writer)
            self.downloads += 1
            self.update_title()
            writer.close()
            await writer.wait_closed()

    def update_title(self):
        os.system(f"title TorNet - {self.targs[2]} - {self.downloads} скачали - Раздача")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="TorNet",
        description="Best torrent client!"
    )
    parser.add_argument("torrent", help="Path to torrent file")
    args = parser.parse_args()

    server = Server()
    asyncio.run(server.start(args.torrent))
