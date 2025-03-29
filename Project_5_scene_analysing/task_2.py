import cv2
import numpy as np


def find_count(image_hsv):
    
    coords = []
    
    hsv_low = (25, 0, 235)
    hsv_high = (40, 256, 256) 
    borders_area = cv2.inRange(image_hsv, hsv_low, hsv_high)
    temp = 2
    
    for i in range(len(borders_area[10]) - 1):
        if borders_area[10][i] != borders_area[10][i + 1]:
            coords.append(i + 1)
            temp += 1
    
    return coords, temp / 2



def find_road_number(image: np.ndarray) -> int:
    """
    Найти номер дороги, на которой нет препятсвия в конце пути.

    :param image: исходное изображение
    :return: номер дороги, на котором нет препятсвия на дороге
    """
    road_number = None
    
    image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    coords, count_borders = find_count(image_hsv)
    coords = np.asarray(coords)
    coords = coords.reshape(int(len(coords) / 2), 2)
    
    imgs_list = []
    for i in range(int(count_borders - 1)):
        imgs_list.append(image_hsv[:, coords[i,0] : coords[i,1], :])
   
    message = 'error'
    for i in range(len(imgs_list)):
        
        hsv_low = (0, 200, 200)
        hsv_high = (8, 256, 256)
        red_detection = cv2.inRange(imgs_list[i], hsv_low, hsv_high)
        
        if np.count_nonzero(red_detection) == 0:
            
            hsv_low = (90, 150, 150)
            hsv_high = (130, 256, 256)
            blue_detection = cv2.inRange(imgs_list[i], hsv_low, hsv_high)
            
            if np.count_nonzero(blue_detection) == 0:
                road_number = i
                message = f'Нужно перестроиться на дорогу номер {road_number}'
            
            else:
                message = 'Перестраиваться не нужно'
    
    return message
