import os
import subprocess
from pychemovality.classes import FilePathManager
from sys import platform


def create_filepath_manager(root_dir, output_molecule_title):
    root_dir = os.path.join(root_dir, "pychemovality")
    output_dir = os.path.join(root_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_xyzr_file_path = os.path.join(output_dir, f"{output_molecule_title}.xyzr")
    sphf = os.path.join(output_dir, f"{output_molecule_title}.SPH")
    if "win" in platform:
        calc_script = os.path.join(root_dir, "fortran", "gepol93_with_args.exe")
    else:
        calc_script = os.path.join(root_dir, "fortran", "gepol93_with_args.out")
        subprocess.check_output(f"chmod +x {calc_script}", shell=True)

    pdb_file = os.path.join(root_dir, f"../input", f"{output_molecule_title}.pdb")
    out_calc_log_file = os.path.join(output_dir, "output_calc_log.txt")
    fpm = FilePathManager(
        root_dir,
        output_molecule_title,
        output_dir,
        output_xyzr_file_path,
        sphf,
        calc_script,
        pdb_file,
        out_calc_log_file,
    )

    return fpm


def remove_existing_log_file(out_calc_log_file):
    if os.path.exists(out_calc_log_file):
        os.remove(out_calc_log_file)
