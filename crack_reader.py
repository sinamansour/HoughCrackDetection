import numpy as np
import pandas as pd
import cv2 as cv
import math as mt
########################### initial properties #############################
filename='15150300.bmp'
image=cv.imread(filename,0)
df=pd.read_csv('point.csv')
point=df.values
raw=np.zeros((image.shape[0],image.shape[1]),dtype='uint8')
# midpoint demonstration:
for i,j,k in point:
    raw[int(i),int(j)]=255
board=cv.cvtColor(raw,cv.COLOR_GRAY2BGR)
df=df.sort_values(by=['r','c'])
df=df.loc[(df.theta>-1.15) & (df.theta < 1.15)]
df.reset_index(drop=True,inplace=True)
df=df.sort_values(by=['c'])
#df=df[:][::2]
df=df.sort_values(by=['r','c'])
df.reset_index(drop=True,inplace=True)
############################################################################
point=df.values
###################### mask properties ###################
mask=np.array([[df.r[0],df.c[0]]],dtype=int)
radius=20
interval=10
for N in range(df.shape[0]):
    rn=int(df.r[N])
    cn=int(df.c[N])

    cv.circle(board,(int(cn),int(rn)),radius=4,color=(255,0,0),thickness=2)
    cv.imshow('outputs/board + mask',board)
    cv.waitKey(1)

    Tt=df.theta[N]
    if len(np.where((mask == (rn,cn)).all(axis=1))[0]) >= 1:
        for r in range(image.shape[0]):
            for c in range(image.shape[1]):
                if mt.sqrt(mt.pow((rn-r),2)+mt.pow((cn-c),2)) < radius:
                    #collecting data
                    slope=mt.tan(Tt)
                    intercept=cn-slope*rn
                    if c-slope*r<intercept+interval and c-slope*r>intercept-interval:
                        board[int(r),int(c),2]=255 #2 is R
                        cv.circle(board,(int(cn),int(rn)),radius=4,color=(255,0,0),thickness=2)
                        # if not len(np.where((mask == (rn,cn)).all(axis=1))[0]) >= 1:
                        mask=np.vstack([mask,[int(r), int(c)]])

        '''ATTENTION: circle method in openCV is set to get inputs based on real coordinate(x,y) ,
        while images coordinate is based on (r,c) coordinate'''
    
    cv.imshow('outputs/board + mask',board)
    cv.waitKey(1)


cv.destroyAllWindows()
# print(df.shape)
# print('mask=\n',mask)
print(mask.shape)