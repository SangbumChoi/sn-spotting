import json
import os

import cv2
import numpy as np

# JSON 파일 경로
json_file_path = "/mnt/nas2/users/sbchoi/sn-spotting/Benchmarks/TemporallyAwarePooling/models/NetVLAD++_run_0/outputs_custom/custom/results_spotting.json"  # 실제 파일 경로로 변경해주세요

# JSON 파일 열기
with open(json_file_path, "r") as json_file:
    # JSON 데이터 읽기
    json_data = json.load(json_file)

# 동영상 파일 경로
video_folder = "/mnt/nas2/users/sbchoi/sn-spotting/Download/data/test/"
half_time = "1"
video_path = os.path.join(video_folder, f"trimmed_{half_time}_HQ.mp4")

# OpenCV로 동영상 읽기
cap = cv2.VideoCapture(video_path)

# 텍스트 내용과 폰트 설정
text = "Hello, World!"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
font_color = (255, 255, 255)  # 흰색

# 동영상 프레임 수 및 프레임 크기 가져오기
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 우측 상단에 텍스트 시각화하는 함수
def visualize_text(frame, text, position_x, position_y):
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_position = (width - text_size[0] - position_x, position_y)
    cv2.putText(
        frame,
        text,
        text_position,
        font,
        font_scale,
        font_color,
        font_thickness,
        cv2.LINE_AA,
    )


# 동영상 출력 설정
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
output_path = os.path.join(video_folder, "output_video.mp4")
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

sorted_data = sorted(json_data["predictions"], key=lambda x: int(x["position"]))
data = [
    entry
    for entry in sorted_data
    if float(entry["confidence"]) > 0.6 and entry["half"] == half_time
]
time = [None] * 60 * 46
for key in data:
    time[int(key["position"]) // 1000] = key

# 프레임별로 반복하여 텍스트 시각화
index = -1
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    index += 1

    if (
        time[int(index // fps)] is not None
        or time[int(index // fps) - 1] is not None
        or time[int(index // fps) + 1] is not None
    ):
        try:
            text = (
                "position: "
                + time[int(index // fps)]["position"]
                + "\n"
                + "label: "
                + time[int(index // fps)]["label"]
                + "\n"
                + "confidence: "
                + time[int(index // fps)]["confidence"]
                + "\n"
                + "gameTime: "
                + time[int(index // fps)]["gameTime"]
            )
            # 텍스트 시각화
            visualize_text(frame, text, 30, 60)
        except:
            print("skip")

        # 동영상 출력
        out.write(frame)
    else:
        if int(index // fps) % 60 == 0:
            print(time[int(index // fps)])
            print(int(index // fps) % 60)

# 리소스 해제
cap.release()
out.release()
cv2.destroyAllWindows()
