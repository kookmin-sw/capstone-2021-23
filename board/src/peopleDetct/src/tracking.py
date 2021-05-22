from scipy.spatial import distance as dist #scipy 는 수학기술
from collections import OrderedDict
import numpy as np

class Trackable:
        def __init__(self, objectID, centroid):
                self.objectID = objectID
                self.centroids = [centroid]
                self.counted = False
# 실제로 트랙킹하는 함수.
class Tracker:
        def __init__(self, maxDisappeared=15): # 생성자.
                self.nextObjectID = 0
                self.objects = OrderedDict()
                self.disappeared = OrderedDict()
                self.maxDisappeared = maxDisappeared
                self.positions = []

        # 새로 사람이 디텍션 되면 등록하고
        def register(self, centroid):
                self.objects[self.nextObjectID] = centroid
                self.disappeared[self.nextObjectID] = 0
                self.nextObjectID += 1

        # 트랙킹 할 필요 없을 때 삭제.
        def deregister(self, objectID):
                del self.objects[objectID]
                del self.disappeared[objectID]
                print('DEREGISTERED : ' + str(objectID))

        # 새로운거 들어오면 레지스터, 필요없으면 디레지스터
        # centriods는 짝짓기 게임처럼 모이는거. 기존 트랙킹 하던
        def update(self, rects):
                # 욜로에서 디텍트된거 사라졌다.
                if len(rects) == 0:
                        for objectID in list(self.disappeared.keys()):
                                self.disappeared[objectID] += 1
                                if self.disappeared[objectID] > self.maxDisappeared: # 50번을 기다리다가 비로소. 왜 50번? 중간중간 놓칠수도있음.
                                        self.deregister(objectID)

                        return self.objects

                # 새로들어온거 0으로 마킹함.
                inputCentroids = np.zeros((len(rects), 2), dtype="int")

                # 디텍션된거(1개가 될수도 여러개가 될수도), 사람 2명이면 2개.
                for (i, (startX, startY, endX, endY)) in enumerate(rects):
                        cX = int((startX + endX) / 2.0)
                        cY = int((startY + endY) / 2.0)
                        inputCentroids[i] = (cX, cY) # 중간점 계산.

                if len(self.objects) == 0:
                        for i in range(0, len(inputCentroids)):
                                self.register(inputCentroids[i])
                else:
                        objectIDs = list(self.objects.keys())
                        objectCentroids = list(self.objects.values())
                        # 디스턴스 구해줌.
                        D = dist.cdist(np.array(objectCentroids), inputCentroids)

                        rows = D.min(axis=1).argsort()
                        cols = D.argmin(axis=1)[rows]

                        usedRows = set()
                        usedCols = set()

                        for (row, col) in zip(rows, cols):
                                if row in usedRows or col in usedCols:
                                        continue

                                objectID = objectIDs[row]
                                self.objects[objectID] = inputCentroids[col]
                                self.disappeared[objectID] = 0

                                usedRows.add(row)
                                usedCols.add(col)

                        unusedRows = set(range(0, D.shape[0])).difference(usedRows)
                        unusedCols = set(range(0, D.shape[1])).difference(usedCols)

                        #print('#############################################')
                        #print('np.array(objectCentroids) : ', np.array(objectCentroids), ' inputCentroids : ', inputCentroids)
                        #print('D : ', D, ' rows : ', rows, ' cols : ', cols)
                        #print('D.shape[0] : ', D.shape[0], ' D.shape[1] : ', D.shape[1]) # 새로 들어온거 없고 있는거 가지고 디텍팅하는거.
                        #print('usedRows : ', usedRows, ' usedCols : ', usedCols)
                        #print('unusedRows : ', unusedRows, ' unusedCols : ', unusedCols)

                        if D.shape[0] >= D.shape[1]:
                                for row in unusedRows:
                                        objectID = objectIDs[row]
                                        self.disappeared[objectID] += 1

                                        if self.disappeared[objectID] > self.maxDisappeared:
                                                self.deregister(objectID)
                        else:
                                for col in unusedCols:
                                        self.register(inputCentroids[col])

                return self.objects
