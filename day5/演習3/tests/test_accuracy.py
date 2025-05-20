import os
import pytest
import glob
from datetime import datetime

ACCURACY_DIR = os.path.join(os.path.dirname(__file__), "accuracy")
ACCURACY_PATH = os.path.join(ACCURACY_DIR, "accuracy.txt")


def read_accuracy(path):
    try:
        with open(path) as f:
            return float(f.read().strip())
    except Exception:
        return None


def get_latest_file_by_datetime(directory):
    files = glob.glob(os.path.join(directory, "*"))
    latest_file = None
    latest_dt = None
    for file in files:
        basename = os.path.basename(file)
        try:
            dt = datetime.strptime(basename, "%Y%m%d_%H%M%S")
            if latest_dt is None or dt > latest_dt:
                latest_dt = dt
                latest_file = file
        except ValueError:
            continue
    return latest_file


latest_file = get_latest_file_by_datetime(ACCURACY_DIR)
prev = read_accuracy(ACCURACY_PATH)
curr = read_accuracy(latest_file) if latest_file else None


def test_accuracy():
    """精度の比較を行う"""
    if prev is None:
        print("前回の推論精度情報がありません。精度比較フローをスキップします。")
        return

    assert curr >= prev, "前回の推論精度から低下しました。"


with open(ACCURACY_PATH, "w") as f:
    f.write(str(curr))