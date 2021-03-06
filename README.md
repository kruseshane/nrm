# NRRD Resolution Manager
nrm is a python script for managing the resolution of an NRRD file.
### Dependencies 
[pynrrd](https://pypi.org/project/pynrrd/)  
[numpy](https://numpy.org/)
### Example usage
`/> nrm.py [.nrrd input file] [.nrrd output file] [slice step]`
### Slice Step?
The "slice step" refers to the amount of data slices stepped over. For example is 5 is made to be the "slice step", then every 5th slice will be taken from the input NRRD file.
