import subprocess
import time


class VPNManager:
    def __init__(self, vpn_name: str):
        self.vpn_name = vpn_name

    def _run_cmd(self, cmd):
        """Run a shell command and return stdout as text."""
        try:
            return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            return e.output

    def is_active(self) -> bool:
        """Return True if the VPN is currently active."""
        output = self._run_cmd(
            ["nmcli", "-t", "-f", "NAME,TYPE,DEVICE", "connection", "show", "--active"]
        )

        for line in output.splitlines():
            fields = line.split(":")
            if len(fields) >= 3:
                name, ctype, device = fields
                if name == self.vpn_name and ctype == "vpn":
                    return True
        return False

    def enable(self) -> bool:
        """Try to activate the VPN. Returns True if successful."""
        output = self._run_cmd(["nmcli", "connection", "up", self.vpn_name])
        time.sleep(5)
        return self.is_active()

    def ensure_enabled(self) -> bool:
        """
        Check if VPN is active, and enable if not.
        Returns True if VPN ends up active.
        """
        if self.is_active():
            return True

        return self.enable()

