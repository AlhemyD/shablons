import unittest
from main import app
from datetime import datetime
import json

"""
Набор модульных тестов osv_report
"""
class test_osv_routes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_osv_report(self):
        # Подготовка
        start_date = '2023-01-01'
        end_date = '2027-12-31'
        storage_id = 'example_storage_id'

        # Действие
        response = self.client.get(f"/api/osv_report?start_date={start_date}&end_date={end_date}&storage_id={storage_id}")
        result = json.loads(response.text)
        # Проверки
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(result)