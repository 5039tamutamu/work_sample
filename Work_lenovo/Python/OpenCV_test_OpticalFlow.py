import numpy as np 
import cv2  # カメラキャプチャの宣言 
cap = cv2.VideoCapture(0) # 一回読み込んでグレーにしてとかいう準備 
_, frame1 = cap.read() 
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY) 
hsv = np.zeros_like(frame1) 
hsv[...,1] = 255  
while(1):  # 現在フレームを取得してグレースケール  
    _, frame2 = cap.read()  
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)  # Farnebackの手法でオプティカルフローを計算  
    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)   # フローの向きを色相にマップする  
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])  
    hsv[...,0] = ang*180/np.pi/2  
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)  
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)   # 表示  
    cv2.imshow("frame", frame2)  
    cv2.imshow("Calculated Opt Flow", rgb)   # escが入ったら終了   
    k = cv2.waitKey(0)  
    if k == 27:  break  # 現在フレームの画像を次の基準画像にする  
    prvs = next  
cap.release() 
cv2.destroyAllWindows()