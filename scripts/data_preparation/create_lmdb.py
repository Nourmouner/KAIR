import sys
import os

# Get the absolute path of the KAIR directory
KAIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Add KAIR to sys.path
sys.path.append(KAIR_PATH)

from utils.utils_video import scandir  # Now it should work!

import lmdb
import cv2
import argparse
from pathlib import Path

def create_lmdb(dataroot, save_path):
    """Create an LMDB dataset from images in a folder."""
    dataroot = Path(dataroot)
    if not dataroot.exists():
        raise FileNotFoundError(f"Dataset folder {dataroot} does not exist!")

    img_paths = sorted(dataroot.glob("*.png"))  # Adjust for your image format
    if not img_paths:
        raise ValueError(f"No images found in {dataroot}")

    # Estimate size of LMDB
    total_size = sum(os.path.getsize(str(p)) for p in img_paths)
    map_size = total_size * 2  # Allocate extra space

    # Create LMDB database
    env = lmdb.open(str(save_path), map_size=map_size)
    with env.begin(write=True) as txn:
        for idx, img_path in enumerate(img_paths):
            with open(img_path, "rb") as f:
                img_data = f.read()
            key = f"{idx:08d}".encode("ascii")
            txn.put(key, img_data)
            print(f"Added {img_path.name} to LMDB")

    env.close()
    print(f"LMDB created at {save_path}")

# Argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert image dataset to LMDB")
    parser.add_argument("--dataroot", type=str, required=True, help="Path to dataset folder")
    parser.add_argument("--save_path", type=str, required=True, help="Path to save LMDB file")

    args = parser.parse_args()
    create_lmdb(args.dataroot, args.save_path)