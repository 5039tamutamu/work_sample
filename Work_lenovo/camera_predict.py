#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import argparse
import torch
import cv2 as cv
import numpy as np
import mediapipe as mp
import time
import os
from util import CvFpsCalc
from util.ParseData import *
from util.Mydataset import *
import torch.optim as optim
from torchinfo import summary
from model.network import *

signlang = ['Good afternoon.', 'Thank you.', 'You are welcome.', 'Nice to meet you.', 'It is a pleasure to meet you.', 'I see.', 'Two person.', 'I am thinking.', 'Good job.', 'Good morning.', 'Good evening.', 'See you again.', 'See you next week.', 'See you tomorrow.']

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=1920)
    parser.add_argument("--height", help='cap height', type=int, default=1080)

    parser.add_argument("--model_complexity",
                        help='model_complexity(0,1(default),2)',
                        type=int,
                        default=1)
    parser.add_argument("--min_detection_confidence",
                        help='face mesh min_detection_confidence',
                        type=float,
                        default=0.5)
    parser.add_argument("--min_tracking_confidence",
                        help='face mesh min_tracking_confidence',
                        type=int,
                        default=0.5)

    parser.add_argument('--use_brect', action='store_true')

    args = parser.parse_args()

    return args

def init_model(data_cfg):

    class_num = 14

    model = DG_STA(class_num, 0.2)
    model = torch.nn.DataParallel(model).cuda()
    # print(model)

    return model

def sample_frame(data_num, time_len):
    #sample #time_len frames from whole video
    sample_size = time_len
    each_num = (data_num - 1) / (sample_size - 1)
    idx_list = [0, data_num - 1]
    for i in range(sample_size):
        index = round(each_num * i)
        if index not in idx_list and index < data_num:
            idx_list.append(index)
    idx_list.sort()

    while len(idx_list) < sample_size:
        idx = random.randint(0, data_num - 1)
        if idx not in idx_list:
            idx_list.append(idx)
    idx_list.sort()

    return idx_list

def getitem(data):
    data_ele = data

    #hand skeleton
    skeleton = data_ele["skeleton"]
    skeleton = np.array(skeleton)

    # sample time_len frames from whole video
    data_num = skeleton.shape[0]
    idx_list = sample_frame(data_num, time_len = 8)
    skeleton = [skeleton[idx] for idx in idx_list]
    skeleton = np.array(skeleton)

    #normalize by palm center
    skeleton -= skeleton[0][1]

    skeleton = torch.from_numpy(skeleton).float()
    # print(skeleton.shape)
    # label
    # label = data_ele["label"] - 1 #

    sample = {'skeleton': skeleton}

    return sample

def parse_data(src_file):
    video = []
    for line in src_file:
        line = line.split("\n")[0]
        data = line.split(" ")
        frame = []
        point = []
        for data_ele in data:
            point.append(float(data_ele))
            if len(point) == 2:
                frame.append(point)
                point = []
        video.append(frame)
    return video

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

def main():
    # 引数解析 #################################################################
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    model_complexity = args.model_complexity
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    use_brect = args.use_brect
    txt_path = 'F:/lab/code/2022/test/test.txt'


    # カメラ準備 ###############################################################
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # モデルロード #############################################################
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic(
        model_complexity=model_complexity,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    # FPS計測モジュール ########################################################
    cvFpsCalc = CvFpsCalc(buffer_len=10)
    time_start = time.time()

    while True:
        display_fps = cvFpsCalc.get()

        # カメラキャプチャ #####################################################
        ret, image = cap.read()
        # image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
        if not ret:
            break
        image = cv.flip(image, 1)  # ミラー表示
        debug_image = copy.deepcopy(image)

        # 検出実施 #############################################################
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = holistic.process(image)
        image.flags.writeable = True
        #検出座標配列
        loglist = []
        # Pose ###############################################################
        pose_landmarks = results.pose_landmarks
        if pose_landmarks is not None:
            # 外接矩形の計算
            brect = calc_bounding_rect(debug_image, pose_landmarks)
            # 描画
            debug_image = draw_pose_landmarks(
                debug_image,
                pose_landmarks,
            )
            debug_image = draw_bounding_rect(use_brect, debug_image, brect)
            index = 0
            #一部の座標のみ配列に保存
            for landmark in pose_landmarks.landmark:
                if index > 10:
                    loglist = np.append(loglist, landmark.x)
                    loglist = np.append(loglist, landmark.y)
                index += 1

        # Hands ###############################################################
        left_hand_landmarks = results.left_hand_landmarks
        right_hand_landmarks = results.right_hand_landmarks
        index = 0
        #一部の座標のみ配列に保存
        if left_hand_landmarks is not None:
            for landmark in left_hand_landmarks.landmark:
                if index ==4:
                    loglist = np.append(loglist, landmark.x)
                    loglist = np.append(loglist, landmark.y)
                if index ==8:
                    loglist = np.append(loglist, landmark.x)
                    loglist = np.append(loglist, landmark.y)
                if index ==12:
                    loglist = np.append(loglist, landmark.x)
                    loglist = np.append(loglist, landmark.y)
                if index ==16:
                    loglist = np.append(loglist, landmark.x)
                    loglist = np.append(loglist, landmark.y)
                if index ==20:
                    loglist = np.append(loglist, landmark.x)
                    loglist = np.append(loglist, landmark.y)
                index += 1
        else:
            for i in range(0, 5):
                    loglist = np.append(loglist, 0.0)
                    loglist = np.append(loglist, 0.0)
        right_hand_landmarks = results.right_hand_landmarks
        index = 0
        #一部の座標のみ配列に保存
        if right_hand_landmarks is not None:
            for landmark in right_hand_landmarks.landmark:
                if index ==4:
                    loglist = np.append(loglist, landmark.x)
                    loglist = np.append(loglist, landmark.y)
                if index ==8:
                    loglist = np.append(loglist, landmark.x)
                    loglist = np.append(loglist, landmark.y)
                if index ==12:
                    loglist = np.append(loglist, landmark.x)
                    loglist = np.append(loglist, landmark.y)
                if index ==16:
                    loglist = np.append(loglist, landmark.x)
                    loglist = np.append(loglist, landmark.y)
                if index ==20:
                    loglist = np.append(loglist, landmark.x)
                    loglist = np.append(loglist, landmark.y)
                index += 1 
        else:
            for i in range(0, 5):
                    loglist = np.append(loglist, 0.0)
                    loglist = np.append(loglist, 0.0)

        # 左手
        if left_hand_landmarks is not None:
            # 手の平重心計算
            cx, cy = calc_palm_moment(debug_image, left_hand_landmarks)
            # 外接矩形の計算
            brect = calc_bounding_rect(debug_image, left_hand_landmarks)
            # 描画
            debug_image = draw_hands_landmarks(
                debug_image,
                cx,
                cy,
                left_hand_landmarks,
                'R',
            )
            debug_image = draw_bounding_rect(use_brect, debug_image, brect)
        # 右手
        if right_hand_landmarks is not None:
            # 手の平重心計算
            cx, cy = calc_palm_moment(debug_image, right_hand_landmarks)
            # 外接矩形の計算
            brect = calc_bounding_rect(debug_image, right_hand_landmarks)
            # 描画
            debug_image = draw_hands_landmarks(
                debug_image,
                cx,
                cy,
                right_hand_landmarks,
                'L',
            )
            debug_image = draw_bounding_rect(use_brect, debug_image, brect)

        cv.putText(debug_image, "FPS:" + str(display_fps), (10, 30),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)

        #立ち上げた後5秒待機
        if (time.time() - time_start) < 5:
            cv.putText(debug_image, "Recognition will start after {} sec.".format(int(6 - (time.time() - time_start))), (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv.LINE_AA)
            if os.path.exists(txt_path):
                os.remove(txt_path)
                print("Old test data have been deleted.")
        #5秒以降はloglist配列がtxt_pathのファイルに保存
        elif (time.time() - time_start) < 11:
            logging(loglist, txt_path)
        else:
            break

        # キー処理(ESC：終了) #################################################
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break

        # 画面反映 #############################################################
        cv.imshow('MediaPipe Holistic Demo', debug_image)

    cap.release()
    cv.destroyAllWindows()
    print("succsess End CV2")
    #出力データで検出
    reconition(txt_path)

#データ保存
def logging(datalist, txt_path):
    with open(txt_path, 'a', newline="") as f:
        for i, data in enumerate(datalist):
            if i == len(datalist) - 1:
                f.write(str(data))
            else:
                f.write(str(data) + " ")
        f.write("\n")
    return

def reconition(test_data):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model = init_model(0)
    # load model weights
    with torch.no_grad():
        weights_path = "F:/lab/code/2022/weights/DGT-STA20.pth"
        model.load_state_dict(torch.load(weights_path, map_location=device))
        model.eval()
        # print("good")

        file = open(test_data)
        result = {}
        video = parse_data(file)
        result[0] = video
        sample = {"skeleton":result[0]}
        file.close()
        sample = getitem(sample)
        data = sample["skeleton"].float()

        score = model(data.unsqueeze(0))
        print(score)
        pred_class = torch.argmax(score)
        print('{}'.format(signlang[pred_class + 1]))

def calc_palm_moment(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    palm_array = np.empty((0, 2), int)

    for index, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        if index == 0:  # 手首1
            palm_array = np.append(palm_array, landmark_point, axis=0)
        if index == 1:  # 手首2
            palm_array = np.append(palm_array, landmark_point, axis=0)
        if index == 5:  # 人差指：付け根
            palm_array = np.append(palm_array, landmark_point, axis=0)
        if index == 9:  # 中指：付け根
            palm_array = np.append(palm_array, landmark_point, axis=0)
        if index == 13:  # 薬指：付け根
            palm_array = np.append(palm_array, landmark_point, axis=0)
        if index == 17:  # 小指：付け根
            palm_array = np.append(palm_array, landmark_point, axis=0)
    M = cv.moments(palm_array)
    cx, cy = 0, 0
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

    return cx, cy

def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]

def draw_hands_landmarks(
        image,
        cx,
        cy,
        landmarks,
        handedness_str='R'):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # キーポイント
    for index, landmark in enumerate(landmarks.landmark):
        if landmark.visibility < 0 or landmark.presence < 0:
            continue

        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_z = landmark.z

        landmark_point.append((landmark_x, landmark_y))

        if index == 0:  # 手首1
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 1:  # 手首2
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 2:  # 親指：付け根
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 3:  # 親指：第1関節
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 4:  # 親指：指先
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
            cv.circle(image, (landmark_x, landmark_y), 12, (0, 255, 0), 2)
        if index == 5:  # 人差指：付け根
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 6:  # 人差指：第2関節
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 7:  # 人差指：第1関節
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 8:  # 人差指：指先
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
            cv.circle(image, (landmark_x, landmark_y), 12, (0, 255, 0), 2)
        if index == 9:  # 中指：付け根
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 10:  # 中指：第2関節
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 11:  # 中指：第1関節
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 12:  # 中指：指先
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
            cv.circle(image, (landmark_x, landmark_y), 12, (0, 255, 0), 2)
        if index == 13:  # 薬指：付け根
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 14:  # 薬指：第2関節
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 15:  # 薬指：第1関節
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 16:  # 薬指：指先
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
            cv.circle(image, (landmark_x, landmark_y), 12, (0, 255, 0), 2)
        if index == 17:  # 小指：付け根
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 18:  # 小指：第2関節
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 19:  # 小指：第1関節
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 20:  # 小指：指先
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
            cv.circle(image, (landmark_x, landmark_y), 12, (0, 255, 0), 2)

        # if True:
        #     cv.putText(image, "z:" + str(round(landmark_z, 3)),
        #                (landmark_x - 10, landmark_y - 10),
        #                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
        #                cv.LINE_AA)

    # 接続線
    if len(landmark_point) > 0:
        # 親指
        cv.line(image, landmark_point[2], landmark_point[3], (0, 255, 0), 2)
        cv.line(image, landmark_point[3], landmark_point[4], (0, 255, 0), 2)

        # 人差指
        cv.line(image, landmark_point[5], landmark_point[6], (0, 255, 0), 2)
        cv.line(image, landmark_point[6], landmark_point[7], (0, 255, 0), 2)
        cv.line(image, landmark_point[7], landmark_point[8], (0, 255, 0), 2)

        # 中指
        cv.line(image, landmark_point[9], landmark_point[10], (0, 255, 0), 2)
        cv.line(image, landmark_point[10], landmark_point[11], (0, 255, 0), 2)
        cv.line(image, landmark_point[11], landmark_point[12], (0, 255, 0), 2)

        # 薬指
        cv.line(image, landmark_point[13], landmark_point[14], (0, 255, 0), 2)
        cv.line(image, landmark_point[14], landmark_point[15], (0, 255, 0), 2)
        cv.line(image, landmark_point[15], landmark_point[16], (0, 255, 0), 2)

        # 小指
        cv.line(image, landmark_point[17], landmark_point[18], (0, 255, 0), 2)
        cv.line(image, landmark_point[18], landmark_point[19], (0, 255, 0), 2)
        cv.line(image, landmark_point[19], landmark_point[20], (0, 255, 0), 2)

        # 手の平
        cv.line(image, landmark_point[0], landmark_point[1], (0, 255, 0), 2)
        cv.line(image, landmark_point[1], landmark_point[2], (0, 255, 0), 2)
        cv.line(image, landmark_point[2], landmark_point[5], (0, 255, 0), 2)
        cv.line(image, landmark_point[5], landmark_point[9], (0, 255, 0), 2)
        cv.line(image, landmark_point[9], landmark_point[13], (0, 255, 0), 2)
        cv.line(image, landmark_point[13], landmark_point[17], (0, 255, 0), 2)
        cv.line(image, landmark_point[17], landmark_point[0], (0, 255, 0), 2)

    # 重心 + 左右
    if len(landmark_point) > 0:
        cv.circle(image, (cx, cy), 12, (0, 255, 0), 2)
        cv.putText(image, handedness_str, (cx - 6, cy + 6),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv.LINE_AA)

    return image

def draw_pose_landmarks(
    image,
    landmarks,
    visibility_th=0.5,):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    for index, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_z = landmark.z
        landmark_point.append([landmark.visibility, (landmark_x, landmark_y)])

        if landmark.visibility < visibility_th:
            continue

        if index == 0:  # 鼻
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 1:  # 右目：目頭
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 2:  # 右目：瞳
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 3:  # 右目：目尻
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 4:  # 左目：目頭
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 5:  # 左目：瞳
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 6:  # 左目：目尻
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 7:  # 右耳
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 8:  # 左耳
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 9:  # 口：左端
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 10:  # 口：左端
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 11:  # 右肩
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 12:  # 左肩
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 13:  # 右肘
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 14:  # 左肘
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 15:  # 右手首
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 16:  # 左手首
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 17:  # 右手1(外側端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 18:  # 左手1(外側端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 19:  # 右手2(先端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 20:  # 左手2(先端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 21:  # 右手3(内側端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 22:  # 左手3(内側端)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 23:  # 腰(右側)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 24:  # 腰(左側)
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 25:  # 右ひざ
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 26:  # 左ひざ
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 27:  # 右足首
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 28:  # 左足首
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 29:  # 右かかと
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 30:  # 左かかと
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 31:  # 右つま先
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
        if index == 32:  # 左つま先
            cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)

        # if True:
        #     cv.putText(image, "z:" + str(round(landmark_z, 3)),
        #                (landmark_x - 10, landmark_y - 10),
        #                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
        #                cv.LINE_AA)

    if len(landmark_point) > 0:
        # 右目
        if landmark_point[1][0] > visibility_th and landmark_point[2][
                0] > visibility_th:
            cv.line(image, landmark_point[1][1], landmark_point[2][1],
                    (0, 255, 0), 2)
        if landmark_point[2][0] > visibility_th and landmark_point[3][
                0] > visibility_th:
            cv.line(image, landmark_point[2][1], landmark_point[3][1],
                    (0, 255, 0), 2)

        # 左目
        if landmark_point[4][0] > visibility_th and landmark_point[5][
                0] > visibility_th:
            cv.line(image, landmark_point[4][1], landmark_point[5][1],
                    (0, 255, 0), 2)
        if landmark_point[5][0] > visibility_th and landmark_point[6][
                0] > visibility_th:
            cv.line(image, landmark_point[5][1], landmark_point[6][1],
                    (0, 255, 0), 2)

        # 口
        if landmark_point[9][0] > visibility_th and landmark_point[10][
                0] > visibility_th:
            cv.line(image, landmark_point[9][1], landmark_point[10][1],
                    (0, 255, 0), 2)

        # 肩
        if landmark_point[11][0] > visibility_th and landmark_point[12][
                0] > visibility_th:
            cv.line(image, landmark_point[11][1], landmark_point[12][1],
                    (0, 255, 0), 2)

        # 右腕
        if landmark_point[11][0] > visibility_th and landmark_point[13][
                0] > visibility_th:
            cv.line(image, landmark_point[11][1], landmark_point[13][1],
                    (0, 255, 0), 2)
        if landmark_point[13][0] > visibility_th and landmark_point[15][
                0] > visibility_th:
            cv.line(image, landmark_point[13][1], landmark_point[15][1],
                    (0, 255, 0), 2)

        # 左腕
        if landmark_point[12][0] > visibility_th and landmark_point[14][
                0] > visibility_th:
            cv.line(image, landmark_point[12][1], landmark_point[14][1],
                    (0, 255, 0), 2)
        if landmark_point[14][0] > visibility_th and landmark_point[16][
                0] > visibility_th:
            cv.line(image, landmark_point[14][1], landmark_point[16][1],
                    (0, 255, 0), 2)

        # 右手
        if landmark_point[15][0] > visibility_th and landmark_point[17][
                0] > visibility_th:
            cv.line(image, landmark_point[15][1], landmark_point[17][1],
                    (0, 255, 0), 2)
        if landmark_point[17][0] > visibility_th and landmark_point[19][
                0] > visibility_th:
            cv.line(image, landmark_point[17][1], landmark_point[19][1],
                    (0, 255, 0), 2)
        if landmark_point[19][0] > visibility_th and landmark_point[21][
                0] > visibility_th:
            cv.line(image, landmark_point[19][1], landmark_point[21][1],
                    (0, 255, 0), 2)
        if landmark_point[21][0] > visibility_th and landmark_point[15][
                0] > visibility_th:
            cv.line(image, landmark_point[21][1], landmark_point[15][1],
                    (0, 255, 0), 2)

        # 左手
        if landmark_point[16][0] > visibility_th and landmark_point[18][
                0] > visibility_th:
            cv.line(image, landmark_point[16][1], landmark_point[18][1],
                    (0, 255, 0), 2)
        if landmark_point[18][0] > visibility_th and landmark_point[20][
                0] > visibility_th:
            cv.line(image, landmark_point[18][1], landmark_point[20][1],
                    (0, 255, 0), 2)
        if landmark_point[20][0] > visibility_th and landmark_point[22][
                0] > visibility_th:
            cv.line(image, landmark_point[20][1], landmark_point[22][1],
                    (0, 255, 0), 2)
        if landmark_point[22][0] > visibility_th and landmark_point[16][
                0] > visibility_th:
            cv.line(image, landmark_point[22][1], landmark_point[16][1],
                    (0, 255, 0), 2)

        # 胴体
        if landmark_point[11][0] > visibility_th and landmark_point[23][
                0] > visibility_th:
            cv.line(image, landmark_point[11][1], landmark_point[23][1],
                    (0, 255, 0), 2)
        if landmark_point[12][0] > visibility_th and landmark_point[24][
                0] > visibility_th:
            cv.line(image, landmark_point[12][1], landmark_point[24][1],
                    (0, 255, 0), 2)
        if landmark_point[23][0] > visibility_th and landmark_point[24][
                0] > visibility_th:
            cv.line(image, landmark_point[23][1], landmark_point[24][1],
                    (0, 255, 0), 2)

        if len(landmark_point) > 25:
            # 右足
            if landmark_point[23][0] > visibility_th and landmark_point[25][
                    0] > visibility_th:
                cv.line(image, landmark_point[23][1], landmark_point[25][1],
                        (0, 255, 0), 2)
            if landmark_point[25][0] > visibility_th and landmark_point[27][
                    0] > visibility_th:
                cv.line(image, landmark_point[25][1], landmark_point[27][1],
                        (0, 255, 0), 2)
            if landmark_point[27][0] > visibility_th and landmark_point[29][
                    0] > visibility_th:
                cv.line(image, landmark_point[27][1], landmark_point[29][1],
                        (0, 255, 0), 2)
            if landmark_point[29][0] > visibility_th and landmark_point[31][
                    0] > visibility_th:
                cv.line(image, landmark_point[29][1], landmark_point[31][1],
                        (0, 255, 0), 2)

            # 左足
            if landmark_point[24][0] > visibility_th and landmark_point[26][
                    0] > visibility_th:
                cv.line(image, landmark_point[24][1], landmark_point[26][1],
                        (0, 255, 0), 2)
            if landmark_point[26][0] > visibility_th and landmark_point[28][
                    0] > visibility_th:
                cv.line(image, landmark_point[26][1], landmark_point[28][1],
                        (0, 255, 0), 2)
            if landmark_point[28][0] > visibility_th and landmark_point[30][
                    0] > visibility_th:
                cv.line(image, landmark_point[28][1], landmark_point[30][1],
                        (0, 255, 0), 2)
            if landmark_point[30][0] > visibility_th and landmark_point[32][
                    0] > visibility_th:
                cv.line(image, landmark_point[30][1], landmark_point[32][1],
                        (0, 255, 0), 2)
    return image

def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        # 外接矩形
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                     (0, 255, 0), 2)

    return image


if __name__ == '__main__':
    main()
