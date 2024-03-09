# pychemovality

[![License](https://img.shields.io/badge/license-BSD-green)](LICENSE.txt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black) 

pychemovality is a python library for estimating the ovality of molecules. 

The library consists of three parts:

1. **Input File Generation**:
This part creates an XYZR file necessary for the calculations downstream. 
XYZ refers to coordinates and R refers to the vanderwaals radii. 
2. **Calculating SES Area and Volume**:
The SES area and volume calculation takes place inside a Fortran executable that is created 
by compiling a modified version of the original [Gepol93](http://www.ccl.net/cca/software/SOURCES/FORTRAN/molecular_surface/gepol93/) Fortran script. 
This script provides the possibility to calculate various molecular surface area such as the Vanderwaals surface area, the molecular surface area and solvent-excluding surface (SES) area and the corresponding volume. For the ovality calculation we use the SES area.
3. **Calculate Ovality**:
Utilize area and volume to calculate ovality

Modifications made to the original Fortran 77 code:

- Bug fixes
- Modified the fortran code to accept sys args from upstream python script
- Modified the fortran code to log all relevant details into a file instead of stdout
- Made the fortran code compatible with latest gfortran for compilation into an executable 



## Usage

Clone the repo and cd into root dir:
```
git clone https://github.com/vandan-revanur/pychemovality 
cd pychemovality
```

Three types of coordinate files can be used as input for calculating ovality.
* XYZ file
* PDB file
* MOL file

To get the ovality of the molecule in your coordinate file run the following:
```
python pychemovality --coord-file-path <path-to-your-coord-file>
```

## Fortran Code Compilation
If you would like to compile the Fortran code residing in the [Fortran](pychemovality/fortran/GEPOL93_modified.FOR) directory of the repo, instructions are available in the [Compilation Instructions](docs/fortran_compilation_instructions.md)


## Authors
* **Vandan Revanur** 

## License

This project is licensed under the BSD License - see the [LICENSE.txt](LICENSE.txt) file for details

## References
[1] Pascual-ahuir, J.L., Silla, E. and Tuñon, I. (1994), GEPOL: An improved description of molecular surfaces. III. A new algorithm for the computation of a solvent-excluding surface. J. Comput. Chem., 15: 1127-1138. https://doi.org/10.1002/jcc.540151009

[2] X-Ability Co. Ltd, 6.19.6 Molecular Surface Area & Volume, Winmostar™ User Manual, Release 11.4.2, Feb 2023, pp 199-200

[3] Pirika, Y. (2011) Properties Estimation: Density: Volume, Surface Area and Ovality estimation with HTML5 program, Density, volume, surface tension and ovality estimation with HTML5 program. Available at: https://www.pirika.com/ENG/TCPE/Den-H5.html (Accessed: March 3, 2023).

[4] Pirika, Y. (2011) Properties Estimation: Estimation of density and volumetric properties, Estimation of density and volumetric properties. Available at: https://pirika.com/ENG/TCPE/Den-Theory.html (Accessed: March 3, 2023). 
