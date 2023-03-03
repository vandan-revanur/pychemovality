# Fortran Code Compilation


**Linux**:

``` 
sudo apt-get install gfortran

gfortran pychemovality/fortran/GEPOL93_modified.FOR -o <path-to-put-the-.out>
```

**OSX**:

``` 
brew install gcc

gfortran pychemovality/fortran/GEPOL93_modified.FOR -o <path-to-put-the-.out>
```



**Windows**:


1. Install Fortran instructions available here: https://fortran-lang.org/en/learn/os_setup/install_gfortran/
2. Add bin folder which contains the gcc and gfortran executables to the PATH variable in your environment variable settings

```
gfortran pychemovality/fortran/GEPOL93_modified.FOR -o <path-to-put-the-.exe>
```

