from pathlib import Path


def read_file(file_path: str):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found:\n{path}"
        )

    if not path.is_file():
        raise ValueError(
            f"The specified path is not a file:\n{path}"
        )

    try:
        return path.read_text(encoding="utf-8")

    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")

        except UnicodeDecodeError:
            raise ValueError(
                "The file is not a readable text file."
            )
