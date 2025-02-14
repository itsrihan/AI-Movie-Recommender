import numpy as np

# Use a raw string to prevent escape sequence errors in the file path
file_path = r"C:\rihan\Projects\Main\AI movie reccomender\Backend\dataset\1b\trainx16x32_15.npz"

# Load the .npz file using numpy.load
npz_data = np.load(file_path, mmap_mode=None, allow_pickle=True, fix_imports=True, encoding='ASCII', max_header_size=10000)

# Print the keys (array names) stored in the .npz file
print("Arrays in the .npz file:", npz_data.files)

# Loop through each key and print the data inside
for key in npz_data.files:
    print(f"\nData in array '{key}':")
    print(npz_data[key])
