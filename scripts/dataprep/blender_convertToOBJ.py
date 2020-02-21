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

root_directory = sys.argv[-3]
root_directory = os.path.abspath(root_directory)
target_faces = int(sys.argv[-2])
export_directory_root = sys.argv[-1]
export_directory_root = os.path.abspath(export_directory_root)

dataset_name = root_directory.split(os.sep)[-1]
#print("dataset_name: " + dataset_name)
newDatasetDir_name = os.path.join(export_directory_root, dataset_name + "_#" + str(target_faces))
#print("newDatasetDir_name: " + newDatasetDir_name)
os.mkdir(newDatasetDir_name)

for rootdir_path, dirs, files in os.walk(root_directory):
    current_path_parts = rootdir_path.split(os.sep)
    for directory in dirs:
        os.mkdir(os.path.join(newDatasetDir_name, directory))
        pass

    for file in files:
        dir_name = current_path_parts[-1]  #This takes into account that the order of direcotries and files in both list are coherent to each other
        #print(os.path.join(rootdir_path, file))
        file_location = os.path.join(rootdir_path, file)
        export_name = os.path.join(newDatasetDir_name, dir_name, file)
        Process(file_location, target_faces, export_name)

#example:
#D:\Windows\Programme\Blender\blender.exe --background --python .\scripts\dataprep\blender_convertToOBJ.py -- .\datasets\Style_Datasets_adjusted\ 500 .\datasets
# the extra " -- " are for blender to stop parsing arguments after