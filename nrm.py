from enum import Enum
import numpy as np
import nrrd
import sys

'''
This python script takes in an nrrd file and spits out a compressed, and potentially sliced, nrrd file
The execution of the script is as follows:

> nrm.py [.nrrd input file] [.nrrd output file] [slice step]

EXAMPLE:
> nrm.py skull.nrrd skull_medium.nrrd 2
'''

class NrrdSizes(Enum):
    XSIZE = 0
    YSIZE = 1
    ZSIZE = 2


original_nrrd_file = sys.argv[1]
converted_nrrd_file = sys.argv[2]

# read nrrd file and parse data and header
try:
    data, header  = nrrd.read(original_nrrd_file)
except FileNotFoundError:
    print(original_nrrd_file, "not found")
    sys.exit()

# size of x, y, and z according to header
x_size = header["sizes"][NrrdSizes.XSIZE.value]
y_size = header["sizes"][NrrdSizes.YSIZE.value]
z_size = header["sizes"][NrrdSizes.ZSIZE.value]

if (original_nrrd_file.split('.')[-1] != "nrrd" or converted_nrrd_file.split('.')[-1] != "nrrd"):
    print("File must be an NRRD")
    sys.exit()

try:
    INDEX_STEP = int(sys.argv[3])

    if INDEX_STEP < 0 and INDEX_STEP > x_size:
        print("Slice step must be positive and less than the number of available slices")
        sys.exit()
except ValueError:
    print("Slice step must be a number")
    sys.exit()

index_lst = [] # list to keep track of indicies containing non-zero data
temp_lst = [] # list to store data and then convert back into 3D np array
y_index = 0 # index of data in x (keep track of y index)

x_index = 0
for x in data:
    # reset and clear index tracking
    y_index = 0
    index_lst.clear()

    for y in x:
        # look for array that is not zero filled
        if not all(e == 0 for e in y):
            index_lst.append(y_index)
        y_index = y_index + 1 # increment here to get 0-based index

    if (INDEX_STEP == 0):
        if len(index_lst) != 0:
            temp_lst.append(x)
    else:
       if len(index_lst) != 0 and x_index % INDEX_STEP == 0:
            temp_lst.append(x)

    x_index = x_index + 1


# Convert temp list to an np array
converted_data = np.array(temp_lst)

# write new nrrd file
nrrd.write(converted_nrrd_file, converted_data)

'''
NOTES:
data[233:278+1, :, :]



'''
