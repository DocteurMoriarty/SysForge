from pathlib import Path
import json
from datetime import datetime

class SSHLogger:
    def __init__(self, log_file: str = "ssh_setup_log.json"):
        self.log_file = Path(log_file)
        self.log_data = {}

    def save(self, server_status: dict, client_status: dict = None):
        """
        Save the SSH server and client status to JSON file with timestamp.
        """
        self.log_data["timestamp"] = datetime.now().isoformat()
        self.log_data["server"] = server_status
        if client_status:
            self.log_data["client"] = client_status

        with open(self.log_file, "w") as f:
            json.dump(self.log_data, f, indent=4)
