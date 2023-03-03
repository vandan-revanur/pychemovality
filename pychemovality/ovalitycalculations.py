import math
import subprocess
import os
from pychemovality.fileoperations import (
    create_filepath_manager,
    remove_existing_log_file,
)
from rdkit.Chem.rdmolfiles import MolFromPDBFile, MolFromXYZFile, MolFromMolFile
from pychemovality.constants import vanderwaals_radii
from pychemovality.classes import AreaVolumeCalculator
from pychemovality.classes import FilePathManager
from typing import Dict, Tuple
from rdkit.Chem.rdchem import Mol


def create_xyzr_file(
    mol: Mol,
    vanderwaals_radii: Dict[str, float],
    fpm: FilePathManager,
):
    """
    Create an XYZR file that will be used downstream for the ovality core calculation.
    XYZ represents coordinates and R represents the vanderwaals radius.

    Parameters
    ----------
    mol:
        Rdkit molecule
    vanderwaals_radii:  Dict[str, float]
        A dictionary with the known vanderwaals radii of atoms in the periodic table
        The values are obtained from here: https://en.wikipedia.org/wiki/Van_der_Waals_radius
    fpm: FilePathManager
        This object holds information about the paths of the various files generated in
        the process of ovality calculation

    """
    conformer = mol.GetConformers()[0]
    num_atoms = 0
    for _ in mol.GetAtoms():
        num_atoms += 1

    lines = [f"*{fpm.output_molecule_title} coordinates file", f"    {num_atoms}"]

    for a in mol.GetAtoms():
        atom_id = a.GetIdx()
        atom_symbol = a.GetSymbol()
        positions = conformer.GetAtomPosition(atom_id)
        x, y, z = positions.x, positions.y, positions.z

        r = vanderwaals_radii[atom_symbol]

        info_string = f"{x:10.5f}{y:10.5f}{z:10.5f}{r:10.5f} {atom_symbol}"
        lines.append(info_string)

    with open(fpm.output_xyzr_file_path, "w") as f:
        for line in lines:
            f.write(f"{line}\n")


def get_area_and_volume_from_output_logs(
    log_calc_txt_file_path: str,
) -> Tuple[float, float]:
    """
    Extract the area and the volume information from the log file created from the calculations.

    Parameters
    ----------
    log_calc_txt_file_path: str
        The path to the log file created from the calculation of the area and volume.

    -------
    Tuple[float, float]
    Area and volume
    """
    with open(log_calc_txt_file_path) as f:
        line_output_file = f.readlines()

    eq_char = line_output_file[-5].find("=")
    star_char = line_output_file[-5].rfind("*")

    area = float(line_output_file[-5][eq_char + 1 : star_char - 1].strip())
    volume = float(line_output_file[-4][eq_char + 1 : star_char - 1].strip())

    return area, volume


def calculate_ovality(area: float, volume: float) -> float:
    """
    Calculate ovality based on the area and the volume.
    Ovality is calculated as a ratio of area to the minimum surface area.
    The minimum surface is the area occupied by a minimal ideal sphere that has the volume specified.

    Parameters
    ----------
    area : float
        Molecular surface area
    volume: float
        Molecular volume

    -------
    float
    Ovality of the molecule.
    """
    minimum_area = (3 * volume) ** (2 / 3) * (4 * math.pi) ** (1 / 3)
    ovality = area / minimum_area

    return ovality


def write_molecular_area_and_volume_to_logs(
    avc: AreaVolumeCalculator, fpm: FilePathManager
):
    """
    Write the molecular surface area and volume calculated into a log

    Parameters
    ----------
    avc: AreaVolumeCalculator
        This object has information related to all attributes required to calculate area and volume
    fpm: FilePathManager
        This object holds information about the paths of the various files generated in
        the process of ovality calculation

    """
    run_string = f"{fpm.calc_script} {fpm.output_molecule_title} {fpm.output_xyzr_file_path} {fpm.sphf} {avc.rd} {avc.ofac} {avc.rmin} {avc.ndiv} {avc.dvec} {avc.vec_file} {avc.display_file} {avc.ksurf} {avc.redu} {avc.pvec} {avc.psph} {avc.pdis} {avc.ass1} {avc.lpr} {fpm.out_calc_log_file}"
    subprocess.check_output(run_string, shell=True)


def get_molecule_name_from_coord_file(coord_filepath: str) -> str:
    """
    Extract the name of the molecule from the coordinate file

    Parameters
    ----------
    coord_filepath : str
        Path to the input coordinate file

    -------
    str
    Name of the molecule
    """
    coord_filename = os.path.basename(coord_filepath)
    output_molecule_title = os.path.splitext(coord_filename)[0]
    return output_molecule_title


def get_mol_from_coord_file(coord_filepath: str) -> Mol:
    """
    Generate an rdkit molecule from the coordinate file path

    Parameters
    ----------
    coord_filepath : str
        Path to the input coordinate file

    -------
    Mol
    rdkit molecule
    """
    coord_filename = os.path.basename(coord_filepath)
    coord_file_ext = os.path.splitext(coord_filename)[1]

    if coord_file_ext == ".xyz":
        mol = MolFromXYZFile(coord_filepath)
    elif coord_file_ext == ".pdb":
        mol = MolFromPDBFile(coord_filepath, removeHs=False)
    elif coord_file_ext == ".mol":
        mol = MolFromMolFile(coord_filepath, removeHs=False)
    else:
        raise NotImplementedError(
            f"The coordinate files of type {coord_file_ext} are not supported"
        )

    return mol


def calculate_area_and_volume(
    root_dir: str, coord_filepath: str
) -> Tuple[float, float]:
    """
    Calculate molecular surface area and volume

    Parameters
    ----------
    root_dir : str
        Path to the root directory
    coord_filepath : str
        Path to the input coordinate file

    -------
    Tuple[float, float]
    area and volume
    """
    mol = get_mol_from_coord_file(coord_filepath)
    output_molecule_title = get_molecule_name_from_coord_file(coord_filepath)
    fpm = create_filepath_manager(root_dir, output_molecule_title)
    remove_existing_log_file(fpm.out_calc_log_file)
    create_xyzr_file(mol, vanderwaals_radii, fpm)

    avc = AreaVolumeCalculator()
    write_molecular_area_and_volume_to_logs(avc, fpm)
    area, volume = get_area_and_volume_from_output_logs(fpm.out_calc_log_file)

    return area, volume


def get_spheroid_type(ovality: float) -> str:
    """
    Get the type of spheroid

    Parameters
    ----------
    ovality : float
        Ovality of the molecule

    -------
    str
    Type of the spheroid either prolate or oblate
    """
    if ovality > 1:
        spheroid_type = "oblate"
    else:
        spheroid_type = "prolate"

    return spheroid_type
