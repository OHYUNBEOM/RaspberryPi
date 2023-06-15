import cv2

# 컬러 이미지
# img=cv2.imread('./Day07/bmw.jpeg')
# 그레이 이미지
#img=cv2.imread('./Day07/bmw.jpeg',cv2.IMREAD_GRAYSCALE)
#cv2.imshow('Original',img)

# 이미지 축소
#img_small=cv2.resize(img,(200,90))
#cv2.imshow('Small',img_small)

# 원본 유지, 흑백 추가
img=cv2.imread('./Day07/bmw.jpeg')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# 이미지 자르기
height,width,channel = img.shape
img_crop=img[:, :int(width/2)]
gray_crop=gray[:, :int(width/2)]

# 이미지 블러
img_blur=cv2.blur(img_crop,(10,10))

cv2.imshow('Blur half',img_blur)
cv2.imshow('Gray half',gray_crop)

cv2.waitKey(0)
cv2.destroyAllWindows()