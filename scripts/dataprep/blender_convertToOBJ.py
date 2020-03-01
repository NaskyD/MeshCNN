import os
import sys
import argparse
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from blender_process import Process

"""
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dataroot', required=True, help='path to meshes')

args = parser.parse_args()
args2 = vars(args)
"""

root_directory = sys.argv[-4]
root_directory = os.path.abspath(root_directory)
target_faces = int(sys.argv[-3])
export_directory_root = sys.argv[-2]
export_directory_root = os.path.abspath(export_directory_root)
test_train_setup = sys.argv[-1]
test_train_setup = test_train_setup == "tt"

dataset_name = root_directory.split(os.sep)[-1]
new_datasetDirRoot_path = os.path.join(export_directory_root, dataset_name + "_#" + str(target_faces))
os.mkdir(new_datasetDirRoot_path)

is_rootDir = True
for rootdir_path, dirs, files in os.walk(root_directory):
    current_path_parts = rootdir_path.split(os.sep)
    current_dir_name = current_path_parts[-1]  # This takes into account that the order of direcotries and files in both list are supposed to be coherent to each other
    categoryDirectory_path = os.path.join(new_datasetDirRoot_path, current_dir_name)

    if is_rootDir:
        for directory in dirs:
            os.mkdir(os.path.join(new_datasetDirRoot_path, directory))
        is_rootDir = False
        continue

    for directory in dirs:
        os.mkdir(os.path.join(categoryDirectory_path, directory))
        #os.makedirs(categoryDirectory_path, exist_ok=True)

    for file in files:
        file_location = os.path.join(rootdir_path, file)
        if test_train_setup:
            export_name = os.path.join(new_datasetDirRoot_path, current_path_parts[-2], current_dir_name,  file)
        else:
            export_name = os.path.join(categoryDirectory_path, file)
        Process(file_location, target_faces, export_name)

#example:
#D:\Windows\Programme\Blender\blender.exe --background --python .\scripts\dataprep\blender_convertToOBJ.py -- .\datasets\Style_Datasets_adjusted\ 500 .\datasets
#D:\_SHARE\MA\projekte\MeshCNN>D:\Windows\Programme\Blender\blender.exe --background --python .\scripts\dataprep\blender_convertToOBJ.py -- .\datasets\shrec_16 2000 .\datasets tt
# the extra " -- " are for blender to stop parsing arguments after