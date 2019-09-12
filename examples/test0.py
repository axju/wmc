import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import distance

path = 'C:/Users/ajura/AppData/Local/Temp/tmp29ngwhnl/test000056.png'
out_path = 'C:/Users/ajura/AppData/Local/Temp/tmp29ngwhnl/test.png'
pw = 'C:/Users/ajura/AppData/Local/Temp/tmp29ngwhnl/pw.png'

img = cv2.imread(path,0)
#edges1 = cv2.Canny(img,100,50)
ret,edges1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
cv2.imwrite('test.png', edges1)


w, h = 18,70 #template.shape[::-1]
template = np.zeros((18,70,3), np.uint8)
cv2.imwrite('template.png', template)
template = cv2.imread('template.png', 0)
template = cv2.putText(template,'PASSWORD', (0,12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
#template = cv2.Canny(template_img,50,50)
#ret,template = cv2.threshold(template,127,255,cv2.THRESH_BINARY)
#w, h = template.shape[::-1]

cv2.imwrite('edges1.png', edges1)
cv2.imwrite('template.png', template)


print('start')
res = cv2.matchTemplate(edges1,template,cv2.TM_CCORR_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
print(min_val, max_val, min_loc, max_loc)

pt = max_loc
cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255,255,255), 2)



"""
#res = cv2.matchTemplate(edges1,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.2
loc = np.where( res >= threshold)


(len(list(zip(*loc[::-1]))))
centers = []
dt = 20
for pt in zip(*loc[::-1]):
    #print(pt[0], pt[1])
    best = [-1,1000]
    for i in range(len(centers)):
        dist = distance.euclidean(pt, centers[i]['center'])
        #print(' ', i, dist)
        if dist < dt and dist < best[1]:
            best = [i, dist]

    if best[0] == -1:
        centers.append({'center': pt, 'points': [pt], 'count': 1})
    else:
        centers[best[0]]['count'] += 1
        centers[best[0]]['points'].append(pt)
        x = sum([p[0] for p in centers[best[0]]['points']])/len(centers[best[0]]['points'])
        y = sum([p[1] for p in centers[best[0]]['points']])/len(centers[best[0]]['points'])
        centers[best[0]]['center'] = [x,y]


centers = sorted(centers, key = lambda i: i['count'])
centers.reverse()

for center in centers:
    print(center)

for i, center in enumerate(centers[:10]):
    pt = (int(center['center'][0]), int(center['center'][1]))
    print(center['count'],pt)
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255,255,255), 2)
    cv2.putText(img,str(i),
        (pt[0], pt[1]-20),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255,255,255),
        2)
"""

#for pt in zip(*loc[::-1]):
#    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite(out_path, img)

#plt.subplot(121),plt.imshow(img,cmap = 'gray')
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#plt.show()

"""
img_rgb = cv2.imread(path)
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread(pw,0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.4
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite(out_path, img_rgb)
"""
