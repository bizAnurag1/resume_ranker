import json
import csv
from config import OUTPUT_FOLDER
from src import utils

class ResumeParser:
    def __init__(self, output_folder):
        self.output_folder = output_folder

    def save_as_json(self, data, file_name):
        file_path = f"{self.output_folder}/{file_name}.json"
        utils.save_to_file(file_path, json.dumps(data, indent=4))

    def save_as_csv(self, data_list, file_name):
        file_path = f"{self.output_folder}/{file_name}.csv"
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data_list[0].keys())
            writer.writeheader()
            writer.writerows(data_list)
