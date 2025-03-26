"""Предварительная проверка линтерами"""

import subprocess


def run_linters() -> None:
    """Запускает линтеры для текущей директории"""

    # subprocess.run(["black", "."], check=True)
    subprocess.run(["ruff", "check", "--fix"], check=True)
    subprocess.run(["isort", "."], check=True)
    subprocess.run(["flake8", "."], check=True)
    subprocess.run(["pylint", "."], check=True)
    # subprocess.run(["mypy", "."], check=True)


if __name__ == "__main__":
    run_linters()
