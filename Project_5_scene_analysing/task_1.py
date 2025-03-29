import cv2
import numpy as np


def find_wall(start, area):
        
        temp = [start[0], start[1]]
        wall = 0
        
        while area[temp[0], temp[1]] > 240:
            temp[0] += 1
        while area[temp[0], temp[1]] < 240:
            wall += 1
            temp[0] += 1
        return wall
    
    
def do_step(temp, way, step, end, area) -> None:
        
        if  temp[1] - step > 0 and area[temp[0], temp[1] - step] == 255 and way[temp[0], temp[1] - step] == 0:
            way[temp[0], temp[1] - step] = way[temp[0], temp[1]] + 1
            if way[end[0], end[1]] == 0:
                
                do_step((temp[0], temp[1] - step), way, step, end, area)
                
        if temp[1] + step < len(area) and area[temp[0], temp[1] + step] == 255 and way[temp[0], temp[1] + step] == 0:
            way[temp[0], temp[1] + step] = way[temp[0], temp[1]] + 1
            if way[end[0], end[1]] == 0:
                
                do_step((temp[0], temp[1] + step), way, step, end, area)
                 
        if temp[0] - step > 0 and area[temp[0] - step, temp[1]] == 255 and way[temp[0] - step, temp[1]] == 0:
            way[temp[0] - step, temp[1]] = way[temp[0], temp[1]] + 1
            if way[end[0], end[1]] == 0:
                
                do_step((temp[0] - step, temp[1]), way, step, end, area)
                
        if temp[0] + step < 322 and area[temp[0] + step, temp[1]] == 255 and way[temp[0] + step, temp[1]] == 0:
            way[temp[0] + step, temp[1]] = way[temp[0], temp[1]] + 1
            if way[end[0], end[1]] == 0:
                
                do_step((temp[0] + step, temp[1]), way, step, end, area) 



def find_way_from_maze(image: np.ndarray) -> tuple:
    """
    Найти путь через лабиринт.

    :param image: изображение лабиринта
    :return: координаты пути из лабиринта в виде (x, y), где x и y - это массивы координат
    """
    
    area = cv2.inRange(image, (240, 240, 240), (255, 255, 255))
    y = np.argwhere(area[0] == 255)
    start = (0, (np.sum(y) // len(y)))
    
    wall = find_wall(start, area)
    passage = len(y)

    step = (passage + wall) // 2
    
    y = np.argwhere(area[len(area) - 1] == 255)
    
    end = (len(area) - 1, (np.sum(y) // len(y))) 
    way = np.zeros_like(area)
    way[start[0] + 1, start[1]] = 1

    coords = []
    #temp -  координаты точки
    start = (start[0] + 1, start[1])
    do_step(start, way, step, end, area)
    coords = [end]
    
    temp = end
    while temp != start:
        if way[temp[0], temp[1] - step] == way[temp[0], temp[1]] - 1:
            temp = (temp[0], temp[1] - step)
        
        elif way[temp[0], temp[1] + step] == way[temp[0], temp[1]] - 1:
            temp = (temp[0], temp[1] + step)
        
        elif way[temp[0] - step, temp[1]] == way[temp[0], temp[1]] - 1:
            temp = (temp[0] - step, temp[1])
        
        elif way[temp[0] + step, temp[1]] == way[temp[0], temp[1]] - 1:
            temp = (temp[0] + step, temp[1])
        
        coords.append(temp)
    
    coords = np.asarray(coords)
    coords = coords.T.flatten()
    coords = coords.reshape(2, int(len(coords) / 2))
    
    return coords