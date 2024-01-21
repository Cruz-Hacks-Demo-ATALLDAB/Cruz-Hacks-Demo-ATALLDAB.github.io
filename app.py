import cv2
import imutils
import time

# Initialize background subtractor
bg_subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()

# Initialize HOG descriptor for person detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Source example video
cap = cv2.VideoCapture('1.mov')

# Counters for detected persons during motion and total persons
person_counter = 0
total_people_count = 0
motion_detected = False
counted_during_motion = False
start_time = 0
delay_time = 4  # 1 second delay before checking the number of persons
motion_stopped = True
motion_pause_time = 0.2 # Maximum duration of a pause to be considered part of the same motion event

while cap.isOpened():
    # Read in video
    ret, frame = cap.read()
    if ret:
        frame = imutils.resize(frame, width=min(400, frame.shape[1]))

        # Apply background subtraction
        fg_mask = bg_subtractor.apply(frame)

        # Threshold the foreground mask
        _, thresh = cv2.threshold(fg_mask, 25, 255, cv2.THRESH_BINARY)

        # Find contours in the thresholded mask
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check if motion is detected
        if len(contours) > 0:
            if not motion_detected:
                # Motion has started, reset flags and start timer
                motion_detected = True
                counted_during_motion = False
                start_time = time.time()
                motion_stopped = False
        else:
            if motion_detected and not motion_stopped:
                # Motion has stopped, check if the pause is within the defined limit
                elapsed_time = time.time() - start_time
                if elapsed_time >= motion_pause_time:
                    # Pause is beyond the limit, reset flags and increment total people count
                    motion_stopped = True
                    counted_during_motion = False
                    total_people_count += person_counter
                    person_counter = 0

        # If motion is detected and not counted during the current motion event
        if motion_detected and not counted_during_motion:
            # Check if 1 second has passed since motion began
            elapsed_time = time.time() - start_time
            if elapsed_time >= delay_time:
                # Detecting all the regions
                (regions, _) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(4, 4), scale=1.05)

                # Drawing rectangles on persons
                for (x, y, w, h) in regions:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Increment person counter
                person_counter += len(regions)
                total_people_count += len(regions)
                counted_during_motion = True

        # Display video output
        cv2.putText(frame, f'Persons during motion: {person_counter}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f'Total People Counted: {total_people_count}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow("Motion Detection", frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
