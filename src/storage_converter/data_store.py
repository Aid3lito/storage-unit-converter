import json
import os
import tempfile


def save_json(file_path, data):
    temp_path = None

    try:
        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=file_path.parent,
            prefix=f".{file_path.name}.",
            suffix=".tmp",
            delete=False
        ) as temp_file:
            temp_path = temp_file.name

            json.dump(
                data,
                temp_file,
                ensure_ascii=False,
                indent=2
            )

            temp_file.flush()
            os.fsync(temp_file.fileno())

        os.replace(
            temp_path,
            file_path
        )

        return True

    except OSError:
        if temp_path is not None:
            try:
                os.remove(temp_path)
            except OSError:
                pass

        return False