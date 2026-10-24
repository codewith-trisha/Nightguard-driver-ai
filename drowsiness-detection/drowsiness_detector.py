import cv2
import time
import numpy as np

def main():
    # Load Haar Cascades from the local project folder
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    if face_cascade.empty() or eye_cascade.empty():
        print("Error: Could not load cascade XML files. Make sure they are in the folder.")
        return

    cap = cv2.VideoCapture(0)
    
    # Drowsiness tracking variables
    eyes_closed_start_time = None
    ALERT_THRESHOLD_SECONDS = 2.0  # 2 seconds of continuous eye closure triggers alert
    
    print("Starting NightGuard AI Drowsiness Detector... Press 'q' to exit.")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break
            
        # Flip frame horizontally for a mirror view
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(60, 60))
        
        status_text = "MONITORING ACTIVE"
        status_color = (0, 255, 0) # Green
        eyes_detected = False
        
        for (x, y, w, h) in faces:
            # Draw face bounding box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Region of Interest for eyes (upper half of the face)
            roi_gray = gray[y:y + int(h * 0.6), x:x+w]
            roi_color = frame[y:y + int(h * 0.6), x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=4, minSize=(20, 20))
            
            if len(eyes) >= 1:
                eyes_detected = True
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            
        if len(faces) == 0:
            status_text = "FACE NOT FOUND"
            status_color = (0, 165, 255) # Orange
            eyes_closed_start_time = None
        elif not eyes_detected:
            # Eyes are closed or hidden
            if eyes_closed_start_time is None:
                eyes_closed_start_time = time.time()
            else:
                elapsed = time.time() - eyes_closed_start_time
                if elapsed >= ALERT_THRESHOLD_SECONDS:
                    status_text = f"DROWSINESS ALERT! ({elapsed:.1f}s)"
                    status_color = (0, 0, 255) # Red
                else:
                    status_text = f"EYES CLOSED... ({elapsed:.1f}s)"
                    status_color = (0, 255, 255) # Yellow
        else:
            # Eyes are open, reset timer
            eyes_closed_start_time = None
            status_text = "MONITORING ACTIVE"
            status_color = (0, 255, 0) # Green

        # Display status banner on screen
        cv2.putText(frame, status_text, (30, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
        cv2.imshow("NightGuard AI - Drowsiness Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()