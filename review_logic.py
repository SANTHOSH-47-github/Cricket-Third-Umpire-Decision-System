import cv2
import os
import yaml
import time


def load_config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)


def load_video():
    cfg = load_config()
    path = os.path.join(
        cfg["templates_config"]["templates_dir"],
        cfg["templates_config"]["clips_dir"],
        cfg["templates_config"]["clip_name"]
    )
    return cv2.VideoCapture(path)


def get_sprite(name):
    cfg = load_config()
    return os.path.join(
        cfg["templates_config"]["templates_dir"],
        cfg["templates_config"]["sprites_dir"],
        name
    )


def decision_sequence(decision):
    sequence = ["pending.png", "sponsor.png"]
    time.sleep(1)
    if decision == "out":
        sequence.append("out.png")
    else:
        sequence.append("not out.png")
    return sequence
