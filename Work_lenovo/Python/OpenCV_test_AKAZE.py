import cv2  # カメラキャプチャの宣言 
cap = cv2.VideoCapture(2) # テンプレートの読み込み 
ref = cv2.imread("template.jpg")  # ディテクタを宣言 
detector = cv2.AKAZE_create() 
kpRef, descRef = detector.detectAndCompute(ref, None)  
while(1):  # 現在フレームを取得してグレースケール  
    _, frame = cap.read()  # 特徴量を検出  
    kp, desc = detector.detectAndCompute(frame, None)   # matcherを生成  
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # matchしてソート  
    matches = bf.match(desc,descRef)  
    matches = sorted(matches, key=lambda x:x.distance)    # 表示  
    imgMatch = cv2.drawMatches(frame, kp, ref, kpRef, matches[:30], None, flags=2)  
    cv2.imshow("Matching Result", imgMatch)   # escが入ったら終了   
    k = cv2.waitKey(10)  
    if k == 27: break  
    elif k == ord('s'):   
        cv2.imwrite("frame.jpg", frame)   
        cv2.imwrite("match.jpg", imgMatch)  
        cap.release() 
cv2.destroyAllWindows()