# import the necessary packages
import re
import dlib
import numpy as np
from imutils import paths
import face_recognition
import cv2
from sklearn.cluster import KMeans


# đường dẫn tới data
paths_img = r"F:\CT_codes\faces_clustering_done\data"

print("[INFO] quantifying faces...")
# load danh sách ảnh
imagePaths = list(paths.list_images(paths_img))

# khởi tạo bộ detect faces
detector = dlib.get_frontal_face_detector()


# khởi tạo 3 danh sách rỗng ban đầu
paths_no_faces = [] # list paths chứa ảnh ko thể detect face hoặc ko để embedding
paths_have_faces = [] # list paths chứa ảnh đã detect face theo thứ tự
encodings_faces = [] # list sau convert thành mảng numpy chứa tập các vector tương ứng với mỗi ảnh trong paths_have_faces

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
    print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
    print(imagePath)
    # đọc ảnh
    img = dlib.load_rgb_image(imagePath)


    # giảm kích thước ảnh mà vẫn giữ tỷ lệ
    img = cv2.pyrDown(img)
    img = cv2.pyrDown(img)
    img = cv2.pyrDown(img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    # dets: danh sách các boxs chứa faces
    dets = detector(img, 1)


    print("Number of faces detected: {}".format(len(dets)))

    # không detect được faces
    if len(dets) == 0:
        print("No faces !!")
        paths_no_faces.append(imagePath)
    # detect được faces
    else:
        # duyệt từng face
        for d in dets:
            # lấy giá trị tọa độ box từ đối tượng
            test_string = str(d)
            temp = re.findall(r'\d+', test_string)
            res = list(map(int, temp))

            # bo ảnh sát khuôn mặt, resize về cùng kích thước
            img_box = img[res[1]:res[3], res[0]:res[2]]
            img_box = cv2.resize(img_box, (60, 60))

            # faces encoding -> vector 128D
            en = face_recognition.face_encodings(img_box)
            # không mã hóa đc do: ảnh face mờ, ko rõ mắt, bắt nhầm sang vùng ảnh khác
            if len(en) == 0:
                print("Not encoding !!")
                paths_no_faces.append(imagePath)
            # mã hóa được
            else:
                paths_have_faces.append(imagePath)
                encodings_faces.append(en[0])
    print("___end_img___\n")


# print(len(paths_no_faces))
# print(len(paths_have_faces))
# convert dang numpy để lưu mảng
encodings_faces = np.array(encodings_faces)
# print(encodings_faces.shape)


print("Save img code.")

# save files no faces
file_no_faces = open(r'F:\CT_codes\faces_clustering_done\save_files/files_no_faces.txt', 'w')
for row in paths_no_faces:
    file_no_faces.write(row+"\n")
file_no_faces.close()


# save files have faces
file_have_faces = open(r'F:\CT_codes\faces_clustering_done\save_files/files_have_faces.txt', 'w')
for row in paths_have_faces:
    file_have_faces.write(row+"\n")
file_have_faces.close()


# save file encodings
file_encodings = open(r'F:\CT_codes\faces_clustering_done\save_files/files_encodings.txt', 'w')
for row in encodings_faces:
    np.savetxt(file_encodings, row)
file_encodings.close()


# save shape of encodings
shape_encodings = open(r'F:\CT_codes\faces_clustering_done\save_files/shape.txt', 'w')
shape_encodings.write(str(encodings_faces.shape))
shape_encodings.close()



