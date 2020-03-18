import json
import csv
import os
from pathlib import Path
from model import Participant, Prize, Lottery


class DataInputHandler:
    data_dir = os.environ.get('LOTTERY_DATA', '../data')

    @staticmethod
    def _load_csv_file(name):
        with open(name, 'r') as f:
            return list(csv.DictReader(f))

    @staticmethod
    def _load_json_file(name):
        with open(name, 'r') as f:
            participants = json.load(f)
            return participants

    def load_participants_info(self, format, name):
        file_path = Path(self.data_dir).joinpath(name)

        participants_data = []
        if format == 'csv':
            participants_data = self._load_csv_file(file_path)
        elif format == 'json':
            participants_data = self._load_json_file(file_path)

        return [Participant(p['id'], p['first_name'],
                            p['last_name'], float(p.get('weight', 1)))
                for p in participants_data]

    def load_lottery_template(self, name):
        base_path = Path(self.data_dir).joinpath('lottery_templates')

        if name:
            file_path = base_path.joinpath(name)
        else:
            file_path = sorted(base_path.iterdir())[0]

        with open(file_path, 'r') as f:
            template = json.load(f)
            prizes = [Prize(p['id'], p['name'], p['amount'])
                      for p in template['prizes']]

            return Lottery(template['name'], prizes)