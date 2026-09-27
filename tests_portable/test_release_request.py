"""Release admission checks without Docker or third-party packages."""
import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("release_request", SCRIPTS / "release_request.py")
request = importlib.util.module_from_spec(spec)
spec.loader.exec_module(request)


class ReleaseRequestTests(unittest.TestCase):
    def test_accepts_reviewed_request(self):
        self.assertEqual(self.resolve(), "2026.09.27.130606Z")

    def resolve(self, **overrides):
        args = {"request": {"version": "2026.09.27.130606Z", "reviewed_source_commit": "abc"},
                "parent": "abc", "changed": [request.REQUEST], "ref": "refs/heads/main"}
        args.update(overrides)
        return request.resolve(**args)

    def test_rejects_wrong_parent(self):
        with self.assertRaises(ValueError):
            self.resolve(parent="different")

    def test_rejects_mixed_commit(self):
        with self.assertRaises(ValueError):
            self.resolve(changed=[request.REQUEST, "scripts/build_reports.py"])

    def test_rejects_other_branch(self):
        with self.assertRaises(ValueError):
            self.resolve(ref="refs/heads/test")

    def test_rejects_bad_or_missing_version(self):
        for value in ["", None, "2026.02.30.000000Z", "2026.09.27.130606Z\ninject=1"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.resolve(request={"version": value, "reviewed_source_commit": "abc"})

    def test_rejects_extra_fields(self):
        with self.assertRaises(ValueError):
            self.resolve(request={"version": "2026.09.27.130606Z", "reviewed_source_commit": "abc", "command": "x"})
