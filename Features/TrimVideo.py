import cv2


def trim_video(input_path, output_path, start_time, end_time):
    # 비디오 불러오기
    video_capture = cv2.VideoCapture(input_path)

    # 프레임 속성 확인
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    frames_per_second = int(video_capture.get(5))

    # 비디오 라이터 생성
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 또는 'XVID' 등의 코덱을 사용할 수 있습니다.
    video_writer = cv2.VideoWriter(
        output_path, fourcc, frames_per_second, (frame_width, frame_height)
    )

    # 시작 프레임 설정
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, int(frames_per_second * start_time))

    # 트리밍 시작
    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if (
            not ret
            or video_capture.get(cv2.CAP_PROP_POS_FRAMES) > frames_per_second * end_time
        ):
            break

        # 트리밍된 비디오를 라이터에 기록
        video_writer.write(frame)

    # 리소스 해제
    video_capture.release()
    video_writer.release()
    cv2.destroyAllWindows()


# 사용 예시
input_video_path = "Download/data/test/12_HQ.mp4"
output_video_path = "Download/data/test/trimmed_12_HQ.mp4"
start_time_seconds = 3600 + 11 * 60 + 12  # 시작 시간 (초)
end_time_seconds = 3600 + 11 * 60 + 22  # 종료 시간 (초)

trim_video(input_video_path, output_video_path, start_time_seconds, end_time_seconds)
