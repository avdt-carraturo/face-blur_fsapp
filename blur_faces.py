import cv2
import mediapipe as mp
import os

# FaceDetection “ufficiale” su Mediapipe 1.x
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

face_detector = mp_face_detection.FaceDetection(
    model_selection=1,
    min_detection_confidence=0.6
)

def blur_faces(input_path: str, output_path: str):
    ext = os.path.splitext(input_path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png"]:
        _blur_image(input_path, output_path)
    elif ext in [".mp4", ".mov", ".avi"]:
        _blur_video(input_path, output_path)
    else:
        raise ValueError("Formato non supportato")


def _blur_image(input_path, output_path):
    image = cv2.imread(input_path)
    h, w, _ = image.shape
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detector.process(rgb)

    if results.detections:
        for det in results.detections:
            bbox = det.location_data.relative_bounding_box
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            bw = int(bbox.width * w)
            bh = int(bbox.height * h)

            face = image[y:y+bh, x:x+bw]
            if face.size > 0:
                face = cv2.GaussianBlur(face, (51, 51), 0)
                image[y:y+bh, x:x+bw] = face

    cv2.imwrite(output_path, image)


def _blur_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detector.process(rgb)

        if results.detections:
            for det in results.detections:
                bbox = det.location_data.relative_bounding_box
                x = int(bbox.xmin * width)
                y = int(bbox.ymin * height)
                bw = int(bbox.width * width)
                bh = int(bbox.height * height)

                face = frame[y:y+bh, x:x+bw]
                if face.size > 0:
                    face = cv2.GaussianBlur(face, (51, 51), 0)
                    frame[y:y+bh, x:x+bw] = face

        out.write(frame)

    cap.release()
    out.release()
