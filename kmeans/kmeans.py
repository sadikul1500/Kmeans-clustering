import cv2
import numpy as np
from os.path import join
import os
import random
from random import randint

#l = randint(0, 256)
#print(l)
#cv2.imshow('test', image)




def initializeCentroids(k):
    centroids = np.zeros((k, 3))
    centroids = np.int_(centroids)
    random.seed(2)
    for i in range(centroids.shape[0]):
        centroids[i][0] = randint(0, 256)
        centroids[i][1] = randint(0, 256)
        centroids[i][2] = randint(0, 256)

    return centroids


def getMinDistanceIndex(rgb, centroids):
    #print('dist')
    distance = 10000.0
    index = 0
    for i in range(centroids.shape[0]):
        dist = (((rgb[0] - centroids[i][0])**2) + ((rgb[1] - centroids[i][1])**2) + ((rgb[2] - centroids[i][2])**2))**.5
        if dist < distance:
            distance = dist
            index = i

    return index


def addToCluster(rgb, groups, centroids):
    #print('cluster')
    index = getMinDistanceIndex(rgb, centroids)
    groups[index].append(rgb)

    return groups


def reassignCentroids(centroids, groups):
    #print('reassign start')
    for i in range(centroids.shape[0]):
        length = len(groups[i])
        #print('length ', length)
        if length > 0:
            avarage = [sum(col) for col in zip(*groups[i])]
            #print('avg ', avarage)
            centroids[i][0] = int(avarage[0] / length)
            centroids[i][1] = int(avarage[1] / length)
            centroids[i][2] = int(avarage[2] / length)

    #print('reAssign done')
    return centroids


def checkAccuracy(centroids, temp, threshold):
    accuracy = True
    #print(centroids)
    #print(temp)
    for i in range(centroids.shape[0]):
        dist = (((temp[i][0] - centroids[i][0])**2) + ((temp[i][1] - centroids[i][1])**2) + ((temp[i][2] - centroids[i][2])**2))**.5
        print('dist ', dist)
        if dist > threshold:
            accuracy = False
    #print(accuracy)
    return accuracy


def generateMaskImage(image, centroids, groups):
    print('aschi')
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            r = image[i][j][0]
            g = image[i][j][1]
            b = image[i][j][2]
            rgb = [r, g, b]

            for iter in range(centroids.shape[0]):
                if rgb in groups[iter]:
                    image[i][j][0] = int(centroids[iter][0])
                    image[i][j][1] = int(centroids[iter][1])
                    image[i][j][2] = int(centroids[iter][2])
    print('done')
    return image


if __name__ == '__main__':
    k = int(input('number of clusters:'))
    threshold = 1.2
    max_iter = 1000

    path_real_image = 'G:\\5 th semester\\dbms2\\kMeans'
    real_image = os.listdir(path_real_image)
    number = 0

    for img in real_image:
        image = cv2.imread(join(path_real_image, img))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        output = image

        centroids = initializeCentroids(k)
        groups = [[] for x in range(k)]

        for iter in range(max_iter):
            print('ok')
            groups = [[] for x in range(k)]
            print(iter)
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    r = image[i][j][0]
                    g = image[i][j][1]
                    b = image[i][j][2]
                    rgb = [r, g, b]
                    groups = addToCluster(rgb, groups, centroids)
                    #print(i,j)

            #print(centroids)

            #centroids_temp = centroids
            new_centroids = centroids.copy()
            centroids = reassignCentroids(centroids, groups)

            stop = checkAccuracy(centroids, new_centroids, threshold)

            if stop == True:
                print('breaked')
                break



        output = generateMaskImage(image, centroids, groups)
        print('image generated')
        cv2.imshow('result', output)
        cv2.waitKey(0)

        #cv2.imwrite(os.path.join(path_real_image, str(number)+'.jpg'), img)
        number += 1


