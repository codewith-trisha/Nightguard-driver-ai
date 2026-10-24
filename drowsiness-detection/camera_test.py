"""
camera_test.py  (Stage 1)
Opens the webcam and shows a live preview with resolution, FPS and
average brightness. Press Q or Esc to quit.

Usage:
    python camera_test.py        -> uses camera 0 (default laptop camera)
    python camera_test.py 1      -> uses camera 1 (e.g. an external webcam)
"""

import sys
import time

import cv2

DEFAULT_CAMERA_INDEX = 0
WINDOW_NAME = "Camera Test - press Q or Esc to quit"


def open_camera(index):
    """Open a camera. CAP_DSHOW is a Windows backend that usually opens
    webcams faster and more reliably; if it fails we try the default one."""
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap.release()
        cap = cv2.VideoCapture(index)
    return cap


def main():
    index = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CAMERA_INDEX

    cap = open_camera(index)
    if not cap.isOpened():
        print(f"ERROR: Could not open camera {index}.")
        print("Check: Windows camera privacy settings, other apps using the "
              "camera (Zoom, Teams, browser), or try 'python camera_test.py 1'.")
        sys.exit(1)

    # Ask for 640x480. The camera may choose something close instead.
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Camera {index} opened. Resolution: {width}x{height}")
    print("Showing live preview. Press Q or Esc in the video window to quit.")

    fps = 0.0
    previous_time = time.time()

    while True:
        ok, frame = cap.read()  # ok is False if no frame could be read
        if not ok:
            print("ERROR: Camera opened but no frame was received.")
            break

        # Mirror the image so it behaves like a mirror (easier to test with).
        frame = cv2.flip(frame, 1)

        # FPS = 1 / time between frames, smoothed so the number is readable.
        now = time.time()
        elapsed = now - previous_time
        previous_time = now
        if elapsed > 0:
            instant_fps = 1.0 / elapsed
            fps = instant_fps if fps == 0 else 0.9 * fps + 0.1 * instant_fps

        # Average brightness (0 = black, 255 = white). Useful for night tests.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = gray.mean()

        info = f"{width}x{height}  FPS: {fps:4.1f}  Brightness: {brightness:5.1f}"
        cv2.putText(frame, info, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 255, 0), 2)

        cv2.imshow(WINDOW_NAME, frame)

        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):  # 27 = Esc
            break
        # Also stop if the user closes the window with the X button.
        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Camera released. Test finished.")


if __name__ == "__main__":
    main()
