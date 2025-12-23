import cv2
import os

# Classificatore volti OpenCV
FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def blur_faces(input_path: str, output_path: str):
    ext = os.path.splitext(input_path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png"]:
        _blur_image(input_path, output_path)
    elif ext in [".mp4", ".avi", ".mov"]:
        _blur_video(input_path, output_path)
    else:
        raise ValueError("Formato non supportato")


def _blur_image(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Impossibile leggere il file: {input_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = img[y:y+h, x:x+w]
        face = cv2.GaussianBlur(face, (201, 201), 0)
        img[y:y+h, x:x+w] = face

    cv2.imwrite(output_path, img)


def _blur_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if cap is None:
        raise ValueError(f"Impossibile leggere il file: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (w, h),
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)

        for (x, y, fw, fh) in faces:
            face = frame[y:y+fh, x:x+fw]
            face = cv2.GaussianBlur(face, (51, 51), 0)
            frame[y:y+fh, x:x+fw] = face

        out.write(frame)

    cap.release()
    out.release()
