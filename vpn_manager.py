#!/usr/bin/python3


#############################################################################################
#############################################################################################
#
#   The MIT License (MIT)
#   
#   Copyright (c) 2023 http://odelay.io 
#   
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#   
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#   
#   Contact : <everett@odelay.io>
#  
#   Description : VPN Manager class.  Checks if VPN is enabled, if not, it will enable
#
#   Version History:
#   
#       Date        Description
#     -----------   -----------------------------------------------------------------------
#      27NOV2025     Original Creation
#
###########################################################################################



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

