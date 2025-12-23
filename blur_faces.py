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

def _apply_blur(face_region):
    # Dimensione del blur proporzionale al volto
    k = max(15, (face_region.shape[1]//3)|1)  # sempre dispari
    return cv2.GaussianBlur(face_region, (k, k), 0)


def _blur_image(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Impossibile leggere il file: {input_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        pad = 10
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(img.shape[1], x + w + pad)
        y2 = min(img.shape[0], y + h + pad)

        face = img[y1:y2, x1:x2]
        img[y1:y2, x1:x2] = _apply_blur(face)

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

    prev_faces = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)

        smoothed_faces = []
        for i, (x, y, fw, fh) in enumerate(faces):
            # Smoothing con frame precedente
            if i < len(prev_faces):
                px, py, pfw, pfh = prev_faces[i]
                alpha = 0.6
                x = int(alpha*x + (1-alpha)*px)
                y = int(alpha*y + (1-alpha)*py)
                fw = int(alpha*fw + (1-alpha)*pfw)
                fh = int(alpha*fh + (1-alpha)*pfh)

            # Aggiungi padding
            pad = 10
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(w, x + fw + pad)
            y2 = min(h, y + fh + pad)

            face = frame[y1:y2, x1:x2]
            frame[y1:y2, x1:x2] = _apply_blur(face)

            smoothed_faces.append((x, y, fw, fh))

        prev_faces = smoothed_faces
        out.write(frame)

    cap.release()
    out.release()