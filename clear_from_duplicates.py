#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os

import numpy as np


# In[ ]:


import cv2


# In[ ]:


from itertools import combinations_with_replacement


# In[ ]:


# hash
# http://ceur-ws.org/Vol-2904/81.pdf


# In[ ]:





# In[ ]:


from lib.preparedata.framessimilaritycheck import resize_img, get_hists, get_uniques_imgs


# In[ ]:





# In[ ]:


CWD = os.path.join(os.getcwd(), 'res', 'duplicatedimages')


# In[ ]:


h = list()
w = list()
imagesinfolder = []

for el in os.listdir(CWD):
    if os.path.isdir(os.path.join(CWD, el)) or el.endswith('png'):
        continue

    imagesinfolder.append(os.path.join(CWD, el))
    img = cv2.imread(os.path.join(CWD, el), cv2.IMREAD_UNCHANGED)
    #print(type(img), img.shape, el)
    h.append(img.shape[0])
    w.append(img.shape[1])
    


# In[ ]:


max(h), min(h)


# In[ ]:


max(w), min(w)


# In[ ]:


imagesinfolder


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


unique_imgs, similars = get_uniques_imgs(CWD, 64, 64, 0.7)


# In[ ]:


unique_imgs.keys()


# In[ ]:


similars


# In[ ]:


for el in similars.keys():
    for idx, pth in enumerate(similars[el]):
        if idx > 0:
            tmp_img = cv2.imread(os.path.join(CWD, pth))
            tmp_img = resize_img(tmp_img, 256)
            img = np.hstack((img, tmp_img))
        else:
            img = cv2.imread(os.path.join(CWD, pth))
            img = resize_img(img, 256)
        
    cv2.imshow('similar', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# In[ ]:


cv2.imshow('tt', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


def shifting():
    h, w = img.shape[:2]
    translation_matrix = np.float32([[1, 0, 200], [0, 1, 300]])
    dst = cv2.warpAffine(img, translation_matrix, (w, h))
    cv2.imshow('Изображение, сдвинутое вправо и вниз', dst)
    cv2.waitKey(0)

Первая строка матрицы — [1, 0, tx ], где tx — количество пикселей, на которые мы будем сдвигать изображение влево или вправо. Отрицательное значения tx будет сдвигать изображение влево, положительное — вправо.
Вторая строка матрицы — [ 0, 1, ty], где ty — количество пикселей, на которые мы будем сдвигать изображение вверх или вниз. Отрицательное значения ty будет сдвигать изображение вверх, положительное — вниз. Важно помнить, что данная матрица определяется как массив с плавающей точкой.
# In[ ]:


def rotation():
    (h, w) = img.shape[:2]
    center = (int(w / 2), int(h / 2))
    rotation_matrix = cv2.getRotationMatrix2D(center, -45, 0.6)
    rotated = cv2.warpAffine(img, rotation_matrix, (w, h))


# In[ ]:




