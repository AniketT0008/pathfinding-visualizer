"""
Send motion commands to the ESP32-S3 over WiFi (TCP port 80).

Set ESP32_IP to the address printed by the firmware Serial Monitor.
"""

from __future__ import annotations

import socket
import time
from typing import Iterable

# ---- CONFIG ----
ESP32_IP = "10.0.0.91"  # TODO: replace with your ESP32-S3 IP
ESP32_PORT = 80
TIMEOUT_S = 1.5
GAP_BETWEEN_CMDS_S = 0.05  # tiny pause so the ESP can finish HTTP reply


def send_command(command: str, retries: int = 2) -> bool:
    """Send a single command like FORWARD, LEFT:350, STOP, PING."""
    payload = (command.strip() + "\r\n").encode("utf-8")
    last_err: Exception | None = None

    for attempt in range(retries + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT_S)
        try:
            sock.connect((ESP32_IP, ESP32_PORT))
            sock.sendall(payload)
            # Drain a bit of the HTTP response so the ESP closes cleanly
            try:
                sock.recv(256)
            except OSError:
                pass
            print(f"Sent: {command}")
            time.sleep(GAP_BETWEEN_CMDS_S)
            return True
        except OSError as exc:
            last_err = exc
            print(f"Send failed ({attempt + 1}/{retries + 1}): {exc}")
            time.sleep(0.15)
        finally:
            sock.close()

    print(f"Giving up on '{command}': {last_err}")
    return False


def ping() -> bool:
    return send_command("PING")


def execute_commands(
    commands: Iterable[str],
    dry_run: bool = False,
    stop_at_end: bool = True,
) -> None:
    """
    Run a sequence of timed commands produced by path_to_commands.

    dry_run=True prints without talking to the robot (safe for testing).
    """
    cmds = list(commands)
    if not cmds:
        print("No commands to run.")
        return

    if dry_run:
        print("--- DRY RUN (not sending to ESP32) ---")
        for c in cmds:
            print(f"  {c}")
        if stop_at_end:
            print("  STOP")
        return

    if not ping():
        print("ESP32 not reachable. Check WiFi, IP, and that firmware is running.")
        return

    for c in cmds:
        # Timed commands block on the ESP; wait locally so we don't flood it.
        wait_s = 0.0
        if ":" in c:
            try:
                wait_s = int(c.split(":", 1)[1]) / 1000.0
            except ValueError:
                wait_s = 0.0

        send_command(c)
        if wait_s > 0:
            time.sleep(wait_s + 0.05)

    if stop_at_end:
        send_command("STOP")


if __name__ == "__main__":
    # Quick connectivity check
    ok = ping()
    print("PONG" if ok else "No response — update ESP32_IP / WiFi settings.")
