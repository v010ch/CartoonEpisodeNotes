
import os
import numpy as np
import cv2



def resize_img(inp_img: np.ndarray, new_size: int, crop_type: str = 'center') -> np.ndarray:

    if inp_img.shape[0] > inp_img.shape[1]:    # h > w
        extension = int((inp_img.shape[0] - inp_img.shape[1]) / 2)
        
        ret_img = np.hstack((np.zeros((inp_img.shape[0], extension, inp_img.shape[2]), 
                                      dtype = np.uint8), 
                             inp_img
                            ))
        ret_img = np.hstack((ret_img, np.zeros((inp_img.shape[0], extension, inp_img.shape[2]), 
                                               dtype = np.uint8)
                            ))
        if ret_img.shape[0] != ret_img.shape[1]:
            ret_img = np.hstack((ret_img, np.zeros((inp_img.shape[0], 1, inp_img.shape[2]), 
                                                   dtype = np.uint8)
                                ))
            
        ret_img = cv2.resize(ret_img, 
                            (new_size, new_size), 
                            interpolation = cv2.INTER_AREA
                            )

    else:
    #if inp_img.shape[0] <= inp_img.shape[1]:   # h < w
        if  crop_type not in ('left', 'center', 'right'):
            raise ValueError(f'wrong crop type: {crop_type}')
        
        if crop_type =='left':
            tmp_img = inp_img[:, 0:inp_img.shape[0]]                   # from left
        if crop_type == 'center':
            shift = int((inp_img.shape[1] - inp_img.shape[0])/2)       # in any case (odd or not) stay closer to right border
            tmp_img = inp_img[:, shift:inp_img.shape[1]-shift]         # center
        if crop_type == 'right':
            tmp_img = inp_img[:, inp_img.shape[1] - inp_img.shape[0]:] # from right
            
        if inp_img.shape[0] > new_size:        # h > squre_size
            ret_img = cv2.resize(tmp_img, 
                                 (new_size, new_size), 
                                 interpolation = cv2.INTER_AREA
                                )
        else: # h < square_size
            ret_img = cv2.resize(tmp_img, 
                                 (new_size, new_size), 
                                 interpolation = cv2.INTER_AREA
                                )

    return ret_img




def get_hists(inp_img: np.ndarray, inp_bins: int) -> tuple:
    if inp_img.shape[2] == 3:
        b = cv2.calcHist([inp_img],
                         [0],          #channels
                         None,         #mask
                         [inp_bins],   #histSize
                         [0, 256]      #range
                         )
        g = cv2.calcHist([inp_img],
                         [1],          #channels
                         None,         #mask
                         [inp_bins],   #histSize
                         [0, 256]      #range
                         )
        r = cv2.calcHist([inp_img],
                         [0],          #channels
                         None,         #mask
                         [inp_bins],   #histSize
                         [0, 256]      #range
                         )
        
        return (b, g, r)
    else:
        gray = cv2.calcHist([inp_img],
                         [0],        #channels
                         None,       #mask
                         [inp_bins], #histSize
                         [0, 256]    #range
                         )
        
        return (gray)

    
    
    
def get_uniques_imgs(inp_folder: str, inp_bins: int, inp_square_size: int, inp_threshold: float, inp_method: int = cv2.HISTCMP_CORREL):
    #method = ## HISTCMP_CORREL  ## HISTCMP_CHISQR  ## HISTCMP_INTERSECT  ## HISTCMP_BHATTACHARYYA 
    
    imagesinfolder = []
    # getting list of jpg from folder
    for el in os.listdir(inp_folder):
        if os.path.isdir(os.path.join(inp_folder, el)) or el.endswith('png'):
            continue

        imagesinfolder.append(os.path.join(inp_folder, el))
    
    
    ret_unique_imgs = {}
    ret_similars = {}

    for idx, el in enumerate(imagesinfolder):
        tmp_img = cv2.imread(el, cv2.IMREAD_UNCHANGED)
        tmp_img = resize_img(tmp_img, inp_square_size)

        # calculate hist for current image
        (b, g, r) = get_hists(tmp_img, inp_bins)

        # compare with cnown images
        for img_path, hst in ret_unique_imgs.items():
            similar_b = cv2.compareHist(hst[0], b, inp_method) 
            similar_g = cv2.compareHist(hst[1], g, inp_method) 
            similar_r = cv2.compareHist(hst[2], r, inp_method) 

            similar = similar_b * similar_g * similar_r
            #print(similar)

            if similar > inp_threshold:
                #print('out')
                if el.split('\\')[-1] in ret_similars.keys():
                    ret_similars[el.split('\\')[-1]].append(img_path.split('\\')[-1])
                else:
                    ret_similars[el.split('\\')[-1]] = [el.split('\\')[-1], img_path.split('\\')[-1]]
                break

        else: # after for: if for complited without break
            #print('add')
            ret_unique_imgs[el] = (b, g, r)
            
    return ret_unique_imgs, ret_similars
