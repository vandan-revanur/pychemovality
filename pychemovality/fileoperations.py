import os
import subprocess
from pychemovality.classes import FilePathManager
from sys import platform
import sys


def create_filepath_manager(
    root_dir: str, output_molecule_title: str
) -> FilePathManager:
    """
    Creates a FilePathManager object. This object holds information about the paths of the various files generated in
    the process of ovality calculation

    Parameters
    ----------
    root_dir : str
        Path to the root directory
    output_molecule_title : str
        Name of the molecule in the output log

    -------
    FilePathManager
    A FilePathManager object
    """
    root_dir = os.path.realpath(sys.path[0])
    output_dir = os.path.join(root_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_xyzr_file_path = os.path.join(output_dir, f"{output_molecule_title}.xyzr")
    sphf = os.path.join(output_dir, f"{output_molecule_title}.SPH")

    if platform in ["win32", "win64"]:
        calc_script = os.path.join(root_dir, "fortran", "gepol93_with_args.exe")
    elif platform == "linux":
        calc_script = os.path.join(root_dir, "fortran", "gepol93_with_args_linux.out")
        subprocess.check_output(f"chmod +x {calc_script}", shell=True)
    elif platform == "darwin":
        calc_script = os.path.join(root_dir, "fortran", "gepol93_with_args_osx.out")
        subprocess.check_output(f"chmod +x {calc_script}", shell=True)
    else:
        raise OSError(f"{platform} OS is not supported")

    out_calc_log_file = os.path.join(output_dir, "output_calc_log.txt")
    fpm = FilePathManager(
        root_dir,
        output_molecule_title,
        output_dir,
        output_xyzr_file_path,
        sphf,
        calc_script,
        out_calc_log_file,
    )

    return fpm


def remove_existing_log_file(out_calc_log_file: str):
    """
    Removes the existing log file (if any). This is necessary for the downstream Fortran script to function as intended

    Parameters
    ----------
    out_calc_log_file : str
        Path to the calculation log file

    """
    if os.path.exists(out_calc_log_file):
        os.remove(out_calc_log_file)
