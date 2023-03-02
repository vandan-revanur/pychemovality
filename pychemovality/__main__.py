import os
import argparse
from pychemovality.ovalitycalculations import calculate_ovality, get_spheroid_type

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--coord-file-path", dest="coord_file_path", required=True, type=str
    )

    args = parser.parse_args()
    coord_filepath = args.coord_file_path
    root_dir = os.getcwd()
    print(root_dir)

    ovality = calculate_ovality(root_dir, coord_filepath)

    spheroid_type = get_spheroid_type(ovality)
    print("ovality: ", ovality)
    print("spheroid_type: ", spheroid_type)
