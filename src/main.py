import socket

import click
import pandas as pd


class ServiceConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_data(self, data):
        self.sock.sendall(data.encode("utf-8"))

    def receive_data(self, buffer_size=1024):
        return self.sock.recv(buffer_size).decode("utf-8")

    def close(self):
        self.sock.close()


class CommandError(Exception):
    """Custom exception for command errors."""

    pass


def send_cmd(conn: ServiceConnection, cmd: str):
    conn.send_data(f"{cmd}\n")
    response = conn.receive_data()

    if "RPRT 0" not in response:
        raise CommandError(f"Command '{cmd}' failed with response: {response}")


@click.command()
@click.option("--host", default="localhost", help="Host to connect to")
@click.option("--port", default=4532, help="Port to connect to")
@click.option("--csv", required=True, help="CSV file to read from")
@click.option("--start", default=1, help="Memory start position")
def main(host: str, port: int, csv: str, start: int):
    frame = pd.read_csv(csv)

    conn = ServiceConnection(host, port)
    try:
        tone = 0

        click.echo("Setting up radio VFOA and VFOB modes")

        # Set radio mode for VFOA
        send_cmd(conn, "V VFOA")
        send_cmd(conn, "F 147000000")
        send_cmd(conn, "M FM 0")
        click.confirm("Confirm tone is turned on for VFOA!")

        # Set radio mode for VFOA
        send_cmd(conn, "V VFOB")
        send_cmd(conn, "F 147000000")
        send_cmd(conn, "M FM 0")
        click.confirm("Confirm tone is turned on for VFOB!")

        frame.sort_values(by=["Tone"], inplace=True)
        mem = 0
        for idx, row in frame.iterrows():
            mem = abs(hash(idx)) + start
            print(f"Setting memory {mem}")

            # do the tone first, so accidental tuning on the radio is reset
            if tone != row["Tone"]:
                click.confirm(f"Confirm tone {row["Tone"]}")
                tone = row["Tone"]

            # set output frequency
            send_cmd(conn, "V VFOA")
            send_cmd(conn, f"F {int(row["Output"] * 1000000)}")

            # set input frequency
            send_cmd(conn, "V VFOB")
            send_cmd(conn, f"F {int(row["Input"] * 1000000)}")

            # set split mode
            send_cmd(conn, "S 1 VFOB")

            # set memory number
            send_cmd(conn, f"E {mem}")

            # save current VFOs to memory
            send_cmd(conn, "G FROM_VFO")

        print(f"Finished setting {mem - 1} memories")

        # move back to first memory
        send_cmd(conn, "V MEM")
        send_cmd(conn, "E 1")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
