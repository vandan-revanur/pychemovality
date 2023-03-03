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
from rdkit.Chem import PropertyMol
from pychemovality.classes import FilePathManager
from typing import Dict


def create_xyzr_file(
    mol: PropertyMol, vanderwaals_radii: Dict[str, float], fpm: FilePathManager
):
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


def get_area_and_volume_from_output_logs(log_calc_txt_file_path: str):
    with open(log_calc_txt_file_path) as f:
        line_output_file = f.readlines()

    eq_char = line_output_file[-5].find("=")
    star_char = line_output_file[-5].rfind("*")

    area = float(line_output_file[-5][eq_char + 1 : star_char - 1].strip())
    volume = float(line_output_file[-4][eq_char + 1 : star_char - 1].strip())

    return area, volume


def get_ovality(area: float, volume: float) -> float:
    minimum_area = (3 * volume) ** (2 / 3) * (4 * math.pi) ** (1 / 3)
    ovality = area / minimum_area

    return ovality


def write_molecular_area_and_volume_to_logs(
    avc: AreaVolumeCalculator, fpm: FilePathManager
):
    run_string = f"{fpm.calc_script} {fpm.output_molecule_title} {fpm.output_xyzr_file_path} {fpm.sphf} {avc.rd} {avc.ofac} {avc.rmin} {avc.ndiv} {avc.dvec} {avc.vec_file} {avc.display_file} {avc.ksurf} {avc.redu} {avc.pvec} {avc.psph} {avc.pdis} {avc.ass1} {avc.lpr} {fpm.out_calc_log_file}"
    subprocess.check_output(run_string, shell=True)


def get_molecule_name_from_coord_file(coord_filepath: str):
    coord_filename = os.path.basename(coord_filepath)
    output_molecule_title = os.path.splitext(coord_filename)[0]
    return output_molecule_title


def get_mol_from_coord_file(coord_filepath: str) -> PropertyMol:
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


def calculate_ovality(root_dir: str, coord_filepath: str) -> float:
    mol = get_mol_from_coord_file(coord_filepath)
    output_molecule_title = get_molecule_name_from_coord_file(coord_filepath)
    fpm = create_filepath_manager(root_dir, output_molecule_title)
    remove_existing_log_file(fpm.out_calc_log_file)
    create_xyzr_file(mol, vanderwaals_radii, fpm)

    avc = AreaVolumeCalculator()
    write_molecular_area_and_volume_to_logs(avc, fpm)
    area, volume = get_area_and_volume_from_output_logs(fpm.out_calc_log_file)
    ovality = get_ovality(area, volume)

    return ovality


def get_spheroid_type(ovality: float) -> str:
    if ovality > 1:
        spheroid_type = "oblate"
    else:
        spheroid_type = "prolate"

    return spheroid_type
