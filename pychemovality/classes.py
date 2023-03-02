from dataclasses import dataclass
import os

@dataclass
class FilePathManager():
  root_dir: str
  output_molecule_title : str
  output_dir : str
  output_xyzr_file_path : str
  sphf: str
  calc_script: str
  pdb_file : str
  out_calc_log_file : str



@dataclass
class AreaVolumeCalculator():
  rd = '1.4'
  ofac = '0.8'
  rmin = '0.50'
  ndiv = '3'
  dvec = '1'
  vec_file = 'VECTORS.BIN'
  display_file = 'DISPLAY.BIN'
  ksurf = 'ESURF'
  redu = '0'
  pvec = '0'
  psph = '0'
  pdis = '0'
  ass1 = '0'
  lpr = '0'