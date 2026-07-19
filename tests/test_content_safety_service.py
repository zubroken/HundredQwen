import unittest

from services.content_safety_service import ContentSafetyService


class ContentSafetyServiceTest(unittest.TestCase):
    def test_allows_normal_learning_input(self):
        service = ContentSafetyService(blocked_terms=["forbidden"])

        result = service.check_input("Explain Transformer attention")

        self.assertTrue(result.allowed)
        self.assertEqual(result.risk_level, "low")
        self.assertEqual(result.sanitized_text, "Explain Transformer attention")

    def test_blocks_configured_sensitive_input(self):
        service = ContentSafetyService(blocked_terms=["forbidden"])

        result = service.check_input("Please generate forbidden content")

        self.assertFalse(result.allowed)
        self.assertEqual(result.risk_level, "high")
        self.assertIn("blocked", result.reason)

    def test_blocks_sensitive_output_without_returning_original_text(self):
        service = ContentSafetyService(blocked_terms=["secret-token"])

        result = service.check_output("This contains secret-token")

        self.assertFalse(result.allowed)
        self.assertNotIn("secret-token", result.sanitized_text)


if __name__ == "__main__":
    unittest.main()
