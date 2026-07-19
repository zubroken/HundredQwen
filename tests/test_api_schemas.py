import unittest

import api.schemas as schemas


class ApiSchemasTest(unittest.TestCase):
    def test_legacy_generate_models_are_not_exported(self):
        self.assertFalse(hasattr(schemas, "GenerateRequest"))
        self.assertFalse(hasattr(schemas, "ResourceResponse"))

    def test_zhiwen_create_request_keeps_legacy_page_count_mapping(self):
        req = schemas.ZhiwenCreateRequest.model_validate(
            {"query": "机器学习导论", "theme": "auto", "page_count": 12}
        )

        self.assertEqual(req.detail_level, "detailed")


if __name__ == "__main__":
    unittest.main()
