import cv2

img = cv2.imread('test.png',-1)

print(img)

cv2.imwrite('test_copy.png',img)