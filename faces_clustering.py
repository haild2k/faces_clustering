import glob
import os
import shutil

import numpy as np
import re
from sklearn.cluster import KMeans


file_no_faces = open(r'save_files\files_no_faces.txt', 'r')
tmp = file_no_faces.read()
paths_no_faces = tmp.split("\n")
paths_no_faces.pop()
file_no_faces.close()
# print(len(paths_no_faces))

# load paths have faces
file_have_faces = open(r'save_files\files_have_faces.txt', 'r')
tmp = file_have_faces.read()
paths_have_faces = tmp.split("\n")
paths_have_faces.pop()
file_have_faces.close()
# print(len(paths_have_faces))

# load shape
file_shape = open(r'save_files\shape.txt', 'r')
encoding_shape = file_shape.read()
file_shape.close
temp = re.findall(r'\d+', encoding_shape)
res = list(map(int, temp))
# print(res)
encoding_faces = np.loadtxt(r"save_files\files_encodings.txt").reshape(tuple(res))
# print(type(encoding_faces))
# print(encoding_faces.shape)

# tiến hành phân cụm
cluster = 40
clt = KMeans(n_clusters=cluster)
clt.fit(encoding_faces)


# create folder "static"
os.mkdir("static")
parent_dir = "static"

# tạo folder tương ứng với số cụm sinh ra, folder cuối cùng là folder "cluster" chứa tập ảnh ko thể phân cụm
for cluster_number in range(0, cluster+1):
    directory = str(cluster_number)
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)

# lưu ảnh theo từng cụm tương ứng
for clus in range(0, cluster):
    dst_dir = r"F:\CT_codes\faces_clustering_done\static\\" + str(clus)
    # print("src đích", dst_dir)
    for label in range(0, len(clt.labels_)):
        if clus == clt.labels_[label]:
            src_dir = paths_have_faces[label]
            # print("src gốc:", src_dir)
            for jpgfile in glob.iglob(src_dir):
            # jpgfile = glob.iglob(src_dir)
                shutil.copy(jpgfile, dst_dir)

# lưu folder nhiễu:
dst_dir = r"F:\CT_codes\faces_clustering_done\static\\" + str(cluster)
for path in paths_no_faces:
    for jpgfile in glob.iglob(path):
        # jpgfile = glob.iglob(src_dir)
        shutil.copy(jpgfile, dst_dir)






