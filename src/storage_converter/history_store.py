import json
from . import data_store

def load_history(file_path, max_entries):
    if not file_path.exists():
        return []

    try:
        with file_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        history = []

        for entry in data[:max_entries]:
            if isinstance(entry, str):
                history.append(entry)

        return history

    except (
        OSError,
        json.JSONDecodeError
    ):
        return []


def save_history(file_path, history):
    return data_store.save_json(
        file_path,
        history
    )