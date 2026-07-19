import unittest
from subprocess import CalledProcessError
from unittest.mock import patch

import check_server


class CheckServerTest(unittest.TestCase):
    def test_parse_windows_listener_pid_for_target_port(self):
        output = """\
  TCP    127.0.0.1:9010       0.0.0.0:0              LISTENING       25148
  TCP    127.0.0.1:9011       0.0.0.0:0              LISTENING       99999
"""

        self.assertEqual(check_server.parse_windows_listener_pid(output, 9010), 25148)

    def test_parse_windows_listener_pid_returns_none_when_port_is_not_listening(self):
        output = "  TCP    127.0.0.1:9011       0.0.0.0:0              LISTENING       99999\n"

        self.assertIsNone(check_server.parse_windows_listener_pid(output, 9010))

    def test_windows_netstat_path_does_not_depend_on_path_environment(self):
        path = check_server.windows_netstat_path({"SystemRoot": "C:\\Windows"})

        self.assertEqual(path, r"C:\Windows\System32\netstat.exe")

    def test_parse_tasklist_process_info_reads_process_name(self):
        output = '"python.exe","25148","Console","1","42,000 K"\n'

        self.assertEqual(
            check_server.parse_tasklist_process_info(output),
            {"name": "python.exe", "start_time": None},
        )

    @patch.object(check_server.sys, "platform", "win32")
    @patch("check_server.subprocess.check_output", side_effect=CalledProcessError(1, "tasklist"))
    def test_process_lookup_silently_handles_permission_errors(self, check_output):
        self.assertIsNone(check_server.get_process_info(25148))
        self.assertEqual(check_output.call_args.kwargs["stderr"], check_server.subprocess.DEVNULL)


if __name__ == "__main__":
    unittest.main()
