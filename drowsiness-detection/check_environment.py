"""
check_environment.py  (Stage 1)
Checks that Python and all required libraries are installed correctly.
Run this once now, and again any time something stops working.
"""

import os
import platform
import struct
import sys

# Hides pygame's welcome message so our output stays clean.
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


def report(label, ok, detail=""):
    """Print one result line and return True/False."""
    status = "[ OK ]" if ok else "[FAIL]"
    print(f"{status} {label} {detail}")
    return ok


def main():
    all_ok = True
    print("=== Environment check ===")

    # ---- Python itself ----
    v = sys.version_info
    bits = struct.calcsize("P") * 8
    print(f"Python {v.major}.{v.minor}.{v.micro}, {bits}-bit, "
          f"{platform.system()} {platform.release()}")

    all_ok &= report("Python is 3.11 or 3.12",
                     (3, 11) <= (v.major, v.minor) <= (3, 12))
    all_ok &= report("Python is 64-bit", bits == 64)
    all_ok &= report("Virtual environment is active",
                     sys.prefix != sys.base_prefix)

    # ---- NumPy ----
    try:
        import numpy as np
        all_ok &= report("NumPy", True, f"version {np.__version__}")
    except Exception as e:
        all_ok &= report("NumPy", False, f"-> {e}")

    # ---- OpenCV ----
    try:
        import cv2
        all_ok &= report("OpenCV", True, f"version {cv2.__version__}")
    except Exception as e:
        all_ok &= report("OpenCV", False, f"-> {e}")

    # ---- MediaPipe (we need the Tasks API, not the old mp.solutions) ----
    try:
        import mediapipe as mp
        from mediapipe.tasks.python import vision  # noqa: F401
        all_ok &= report("MediaPipe + Tasks API", True,
                         f"version {mp.__version__}")
        legacy = hasattr(mp, "solutions")
        print(f"       (legacy mp.solutions present: {legacy}; "
              f"this project does not use it)")
    except Exception as e:
        all_ok &= report("MediaPipe + Tasks API", False, f"-> {e}")

    # ---- Pygame and audio output device ----
    try:
        import pygame
        all_ok &= report("Pygame", True, f"version {pygame.version.ver}")
        try:
            pygame.mixer.init()
            report("Audio device (pygame.mixer)", True)
            pygame.mixer.quit()
        except Exception as e:
            all_ok &= report("Audio device (pygame.mixer)", False, f"-> {e}")
    except Exception as e:
        all_ok &= report("Pygame", False, f"-> {e}")

    print()
    if all_ok:
        print("All checks passed. You are ready for the camera test.")
    else:
        print("Some checks failed. See the troubleshooting list in the guide.")


if __name__ == "__main__":
    main()
