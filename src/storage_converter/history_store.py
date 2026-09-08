import json


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
    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with file_path.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            history,
            file,
            ensure_ascii=False,
            indent=2
        )