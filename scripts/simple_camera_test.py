import cv2
import time

print("Testing camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Cannot open camera")
    exit()

print("Camera opened successfully")
print("Showing camera for 5 seconds...")

start_time = time.time()
while (time.time() - start_time) < 5:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Cannot read frame")
        break
    
    cv2.putText(frame, 'Test Camera', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Test', frame)
    
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
print("Test complete")