import json
import unittest

import requests

topo_name_test = "TopoFinal_2.raw"
topo_type_test = "raw"
# model_name_test = "yolo_m_batch_32"
model_name_test = "yolo_n_batch_64"
model_type_test = "yolo"

# Sample unit tests


class TestEjectorAutoDetect(unittest.TestCase):

    def test_01_load_model(self):
        print("Running test: test_load_model")
        url = "http://127.0.0.1:8088/load_model/"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        data = {
            "model_name": f"{model_name_test}",
            "model_type": f"{model_type_test}",
        }
        json_data = json.dumps(data)
        response = requests.post(url, headers=headers, data=json_data)
        print("response = " + str(response.json()))
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", str(response.json()))
        response_data = response.json()
        message = response_data["message"]
        print(f"{message = }")
        self.assertEqual(message, "success")
        data_field = response_data["data"]
        self.assertIsNotNone(data_field)
        self.assertEqual(data_field["model_name"], f"{model_name_test}")
        self.assertEqual(data_field["model_type"], f"{model_type_test}")

    def test_02_auto_detect(self):
        print("Running test: test_auto_detect")
        url = "http://127.0.0.1:8088/detect/"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        data = {
            "topo_name": f"{topo_name_test}",
            "topo_format": f"{topo_type_test}",
        }
        json_data = json.dumps(data)
        response = requests.post(url, headers=headers, data=json_data)
        print("response = " + str(response.json()))
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", str(response.json()))
        response_data = response.json()
        message = response_data["message"]
        print(f"{message = }")
        self.assertEqual(message, "success")
        data_field = response_data["data"]
        self.assertIsNotNone(data_field)
        self.assertEqual(data_field["topo_name"], f"{topo_name_test}")
        self.assertEqual(data_field["topo_format"], f"{topo_type_test}")
        self.assertEqual(
            data_field["mask_name"], f"{topo_name_test.split('.')[0]}.png"
        )
        self.assertEqual(data_field["mask_format"], "png")


if __name__ == "__main__":
    unittest.main()
