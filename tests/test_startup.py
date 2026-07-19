import os
import unittest
from pathlib import Path

import main


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class StartupConfigurationTest(unittest.TestCase):
    def test_main_uses_environment_port_when_cli_port_is_omitted(self):
        self.assertTrue(callable(getattr(main, "resolve_port", None)))
        self.assertEqual(main.resolve_port(None, {"SERVER_PORT": "9022"}), 9022)

    def test_main_prefers_explicit_cli_port(self):
        self.assertTrue(callable(getattr(main, "resolve_port", None)))
        self.assertEqual(main.resolve_port(9010, {"SERVER_PORT": "9022"}), 9010)

    def test_windows_launcher_uses_the_fixed_project_port_without_killing_all_python(self):
        launcher = PROJECT_ROOT / "start.ps1"

        self.assertTrue(launcher.exists())
        content = launcher.read_text(encoding="utf-8")

        self.assertIn("$Port = 9010", content)
        self.assertIn("/api/config/llm/status", content)
        self.assertIn("--port $Port", content)
        self.assertNotIn("taskkill", content.lower())
        self.assertNotIn("Stop-Process -Name python", content)

    def test_windows_launcher_is_ascii_compatible_with_windows_powershell_5(self):
        launcher = PROJECT_ROOT / "start.ps1"

        self.assertTrue(launcher.exists())
        launcher.read_text(encoding="utf-8").encode("ascii")


if __name__ == "__main__":
    unittest.main()
