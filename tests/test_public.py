import pathlib
import unittest

import v4_core_public as v4


class PublicSyntaxTests(unittest.TestCase):
    def test_round_trip(self):
        for namespace in v4.CORE_NAMESPACES:
            with self.subTest(namespace=namespace):
                message = v4.compose(namespace, "QUERY", "example=true", frm="A", to="B")
                result = v4.parse(message)
                self.assertTrue(result["valid"], result["bledy"])
                self.assertEqual(result["payload"], "example=true")

    def test_invalid_messages(self):
        bad = [
            "", "@VERSION[4.0]::ACK::OK[broken",
            "@VERSION[4.0]::ACK::RECEIVED[task] + ETA[2min]",
            "@VERSION[4.0]::CMD::STOP[x] + CMD::NEXT[y]",
            "@VERSION[4.0]::TASK::EXECUTE[job] TTL::300",
            "@VERSION[4.0]@BOGUS[x]::ACK::OK[x]",
            "@FROM[A]@VERSION[4.0]::ACK::OK[x]",
            "@VERSION[4.0]@TO[A]@TO[B]::ACK::OK[x]",
            "@VERSION[4.0]@TO[A]@BROADCAST::ACK::OK[x]",
            "@VERSION[4.0]@SEQ[abc]::ACK::OK[x]",
            "@VERSION[4.0]@PRIORITY[URGENT]::ACK::OK[x]",
            "@VERSION[4.0]@PARALLEL[yes]::ACK::OK[x]",
            "@VERSION[4.0]::PRIVATE::QUERY[x]",
            "@VERSION[4.0]::ACK::OK[x\ny]",
            "@VERSION[4.0]::ACK::OK[x\ry]",
        ]
        for message in bad:
            with self.subTest(message=message):
                self.assertFalse(v4.parse(message)["valid"])

    def test_extensible_commands_and_nested_payload(self):
        result = v4.parse('@VERSION[4.0]::DATA::CUSTOM_2[{"items":[1,2]}]')
        self.assertTrue(result["valid"], result["bledy"])
        self.assertEqual(result["command"], "CUSTOM_2")

    def test_compose_rejects_invalid_input(self):
        with self.assertRaises(v4.V4Error):
            v4.compose("ACK", "OK", "a\nb")
        with self.assertRaises(v4.V4Error):
            v4.compose("ACK", "OK", "x", frm="A]@BOGUS[x")

    def test_documented_examples(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        count = 0
        for name in ("README.md", "skill-jezyk-ai-PL.md", "skill-jezyk-ai-EN.md"):
            for line in (root / name).read_text(encoding="utf-8").splitlines():
                if line.startswith("@VERSION[4.0]") and "::NAMESPACE::" not in line:
                    with self.subTest(file=name, message=line):
                        result = v4.parse(line)
                        self.assertTrue(result["valid"], result["bledy"])
                    count += 1
        self.assertGreaterEqual(count, 10)


if __name__ == "__main__":
    unittest.main()
