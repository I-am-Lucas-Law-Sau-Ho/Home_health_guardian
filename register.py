from tkinter import *
import cv2
import mediapipe as mp
import numpy as np
from tkinter import messagebox 
from matplotlib import pyplot as plt

try:
    import Tkinter as tk
except:
    import tkinter as tk
root = Tk()
root.configure(bg="yellow")
 
root.geometry('400x400')

#just which cam is used to set Q
Q = 0

def reset_entry():
    age_tf.delete(0, 'end')
    height_tf.delete(0, 'end')
    weight_tf.delete(0, 'end')


def calculate_bmi():
    kg = int(weight_tf.get())
    m = int(height_tf.get()) / 100
    bmi = kg / (m * m)
    bmi = round(bmi, 1)
    bmi_index(bmi)


def bmi_index(bmi):
    if bmi < 18.5:
        messagebox.showinfo('bmi-pythonguides', f'BMI = {bmi} is Underweight. We recommand you choose eat healthily')
    elif (bmi > 18.5) and (bmi < 24.9):
        messagebox.showinfo('bmi-pythonguides',
                            f'BMI = {bmi} is Normal we recommand you choose normal mode and eat healthily')
    elif (bmi > 24.9) and (bmi < 29.9):
        messagebox.showinfo('bmi-pythonguides',
                            f'BMI = {bmi} is Overweight we recommand you choose eat healthily and hard mode')
    elif (bmi > 29.9):
        messagebox.showinfo('bmi-pythonguides',
                            f'BMI = {bmi} is Obesity we recommand you choose eat healthily and hard mode')
    else:
        messagebox.showerror('bmi-pythonguides', 'something went wrong!')


var = IntVar()

frame = Frame(root, padx=10, pady=10, bg="orange")
frame.pack(expand=True)


def labeler(e):
    age_lb.config(text="Your height is " + age_lb.get(1.0, END + "-1c") + e.char + " m")

#######nomove###########nomove###############nomove###############nomove###############nomove#############nomove###############nomove##############nomove###################
#######nomove###########nomove###############nomove###############nomove###############nomove#############nomove###############nomove##############nomove###################
#######nomove###########nomove###############nomove###############nomove###############nomove#############nomove###############nomove##############nomove###################
#######nomove###########nomove###############nomove###############nomove###############nomove#############nomove###############nomove##############nomove###################
#######nomove###########nomove###############nomove###############nomove###############nomove#############nomove###############nomove##############nomove###################
def nomove():
    # Initializing mediapipe pose class.
    mp_pose = mp.solutions.pose

    # Setting up the Pose function.
    pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)

    # Initializing mediapipe drawing class, useful for annotation.
    mp_drawing = mp.solutions.drawing_utils

    def detectPose(image, pose, display=True):
        '''
        This function performs pose detection on an image.
        Args:
            image: The input image with a prominent person whose pose landmarks needs to be detected.
            pose: The pose setup function required to perform the pose detection.
            display: A boolean value that is if set to true the function displays the original input image, the resultant image,
                     and the pose landmarks in 3D plot and returns nothing.
        Returns:
            output_image: The input image with the detected pose landmarks drawn.
            landmarks: A list of detected landmarks converted into their original scale.
        '''

        # Create a copy of the input image.
        output_image = image.copy()

        # Convert the image from BGR into RGB format.
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Perform the Pose Detection.
        results = pose.process(imageRGB)

        # Retrieve the height and width of the input image.
        height, width, _ = image.shape

        # Initialize a list to store the detected landmarks.
        landmarks = []

        # Check if any landmarks are detected.
        if results.pose_landmarks:

            # Draw Pose landmarks on the output image.
            mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                      connections=mp_pose.POSE_CONNECTIONS)

            # Iterate over the detected landmarks.
            for landmark in results.pose_landmarks.landmark:
                # Append the landmark into the list.
                landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                  (landmark.z * width)))

        # Check if the original input image and the resultant image are specified to be displayed.
        if display:

            # Display the original input image and the resultant image.
            plt.figure(figsize=[22, 22])
            plt.subplot(121)
            plt.imshow(image[:, :, ::-1])
            plt.imshow(image[:, :, ::-1])
            plt.title("Original Image")
            plt.axis('off')
            plt.subplot(122)
            plt.imshow(output_image[:, :, ::-1])
            plt.title("Output Image")
            plt.axis('off')

            # Also Plot the Pose landmarks in 3D.
            mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

        # Otherwise
        else:

            # Return the output image and the found landmarks.
            return output_image, landmarks

    def calculateAngle(landmark1, landmark2, landmark3):
        '''
        This function calculates angle between three different landmarks.
        Args:
            landmark1: The first landmark containing the x,y and z coordinates.
            landmark2: The second landmark containing the x,y and z coordinates.
            landmark3: The third landmark containing the x,y and z coordinates.
        Returns:
            angle: The calculated angle between the three landmarks.

        '''

        # Get the required landmarks coordinates.
        x1, y1, z1 = landmark1
        x2, y2, z2 = landmark2
        x3, y3, z3 = landmark3

        # Calculate the angle between the three points
        a = [x1, y1, z1]
        b = [x2, y2, z2]
        c = [x3, y3, z3]
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle
        # Check if the angle is less than zero.
        if angle < 0:
            # Add 360 to the found angle.
            angle += 360

        # Return the calculated angle.
        return angle

    def classifyPose(landmarks, output_image, display=False):
        '''
        This function classifies yoga poses depending upon the angles of various body joints.
        Args:
            landmarks: A list of detected landmarks of the person whose pose needs to be classified.
            output_image: A image of the person with the detected pose landmarks drawn.
            display: A boolean value that is if set to true the function displays the resultant image with the pose label
            written on it and returns nothing.
        Returns:
            output_image: The image with the detected pose landmarks drawn and pose label written.
            label: The classified pose label of the person in the output_image.

        '''
        image_height, image_width, _ = output_image.shape

        # Initialize the label of the pose. It is not known at this stage.
        label = 'Unknown Pose'

        # Specify the color (Red) with which the label will be written on the image.
        color = (0, 0, 255)

        # Calculate the required angles.
        # ----------------------------------------------------------------------------------------------------------------

        # Get the angle between the left shoulder, elbow and wrist points.
        left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
        if left_elbow_angle > 180:
            left_elbow_angle = 360 - left_elbow_angle

        # Get the angle between the right shoulder, elbow and wrist points.
        right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])

        if right_elbow_angle > 180:
            right_elbow_angle = 360 - right_elbow_angle
        # Get the angle between the left elbow, shoulder and hip points.
        left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                             landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
        if left_shoulder_angle > 180:
            left_shoulder_angle = 360 - left_shoulder_angle
        # Get the angle between the right hip, shoulder and elbow points.
        right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
        if right_shoulder_angle > 180:
            right_shoulder_angle = 360 - right_shoulder_angle
        # Get the angle between the left hip, knee and ankle points.
        left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
        if left_knee_angle > 180:
            left_knee_angle = 360 - left_knee_angle
        # Get the angle between the right hip, knee and ankle points
        right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
        if right_knee_angle > 180:
            right_knee_angle = 360 - right_knee_angle
        right_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                         landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])
        if right_hip_angle > 180:
            right_hip_angle = 360 - right_hip_angle
        left_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])
        if left_hip_angle > 180:
            left_hip_angle = 360 - left_hip_angle

        # ----------------------------------------------------------------------------------------------------------------

        # Check if it is the warrior II pose or the T pose.
        # As for both of them, both arms should be straight and shoulders should be at the specific angle.
        # ----------------------------------------------------------------------------------------------------------------

        # Check if the both arms are straight.

        # Check if shoulders are at the required angle.

        # Check if it is the warrior II pose.
        # ----------------------------------------------------------------------------------------------------------------

        # Check if one leg is straight.
        if left_knee_angle > 155 and left_knee_angle < 195 or right_knee_angle > 155 and right_knee_angle < 195:

            # Check if the other leg is bended at the required angle.
            if left_knee_angle > 80 and left_knee_angle < 130 or right_knee_angle > 80 and right_knee_angle < 130:
                # Specify the label of the pose that is Warrior II pose.
                label = 'Warrior II Pose'

                # ----------------------------------------------------------------------------------------------------------------

        # Check if it is the T pose.
        # ----------------------------------------------------------------------------------------------------------------

        # Check if both legs are straight
        if left_knee_angle > 160 and left_knee_angle < 180 and right_knee_angle > 160 and right_knee_angle < 180:
            if left_hip_angle > 160 and left_hip_angle < 180 and left_hip_angle > 160 and left_hip_angle < 180:
                if left_elbow_angle > 160 and left_elbow_angle < 180 and left_elbow_angle > 160 and left_elbow_angle < 180:
                    if left_shoulder_angle > 75 and left_shoulder_angle < 120 and left_shoulder_angle > 75 and left_shoulder_angle < 120:
                        # Specify the label of the pose that is tree pose.
                        label = 'T Pose'

        # ----------------------------------------------------------------------------------------------------------------

        # Check if it is the tree pose.
        # ----------------------------------------------------------------------------------------------------------------

        # Check if one leg is straight
        if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

            # Check if the other leg is bended at the required angle.
            if left_knee_angle > 25 and left_knee_angle < 45 or right_knee_angle > 25 and right_knee_angle < 45:
                # Specify the label of the pose that is tree pose.
                label = 'Tree Pose'

        # ----------------------------------------------------------------------------------------------------------------

        # Check if it is the Touch the ground pose.
        # ----------------------------------------------------------------------------------------------------------------

        # Check if both leg is straight
        if left_knee_angle > 160 and left_knee_angle < 200 and right_knee_angle > 160 and right_knee_angle < 200:

            # Check if the body is bended at the required angle.
            if left_hip_angle > 60 and left_hip_angle < 120 and right_hip_angle > 60 and right_hip_angle < 120:

                # check if it is like a downward u shape
                if left_shoulder_angle > 75 and left_shoulder_angle < 120 and right_shoulder_angle > 75 and right_shoulder_angle < 120:
                    # Specify the label of the pose that is tree pose.
                    label = 'Touch the ground'

        # ---------------------------------------------------------------------------------------------------------------

        # Check if the pose is classified successfully
        if label != 'Unknown Pose':
            # Update the color (to green) with which the label will be written on the image.
            color = (0, 255, 0)
            # resize the photo
        output_image = cv2.resize(output_image, (1100, 800))
        # Write the label on the output image.
        if color == (0, 255, 0):
            cv2.rectangle(output_image, (20, 5), (355, 275), (0, 0, 255), -1)
        else:
            cv2.rectangle(output_image, (20, 5), (355, 275), (0, 255, 0), -1)
        cv2.putText(output_image, label, (30, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
        cv2.putText(output_image, " left knee: " + str(round(left_knee_angle)), (10, 60), cv2.FONT_HERSHEY_PLAIN, 2,
                    color, 2)
        cv2.putText(output_image, " right knee: " + str(round(right_knee_angle)), (10, 90), cv2.FONT_HERSHEY_PLAIN, 2,
                    color, 2)
        cv2.putText(output_image, " left elbow: " + str(round(left_elbow_angle)), (10, 120), cv2.FONT_HERSHEY_PLAIN, 2,
                    color, 2)
        cv2.putText(output_image, " right elbow: " + str(round(right_elbow_angle)), (10, 150), cv2.FONT_HERSHEY_PLAIN,
                    2, color, 2)
        cv2.putText(output_image, " left shoulder: " + str(round(left_shoulder_angle)), (10, 180),
                    cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
        cv2.putText(output_image, " right shoulder: " + str(round(right_shoulder_angle)), (10, 210),
                    cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
        cv2.putText(output_image, " right hip: " + str(round(right_hip_angle)), (10, 240), cv2.FONT_HERSHEY_PLAIN, 2,
                    color, 2)
        cv2.putText(output_image, " left hip: " + str(round(left_hip_angle)), (10, 270), cv2.FONT_HERSHEY_PLAIN, 2,
                    color, 2)

        # Check if the resultant image is specified to be displayed.
        if display:

            # Display the resultant image.
            plt.figure(figsize=[10, 10])
            plt.imshow(output_image[:, :, ::-1])
            plt.title("Output Image")
            plt.axis('off')

        else:

            # Return the output image and the classified label.
            return output_image, label

    # Setup Pose function for video.
    pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

    # Initialize the VideoCapture object to read from the webcam.

    camera_video = cv2.VideoCapture(Q, cv2.CAP_DSHOW)
    camera_video.set(3, 1280)
    camera_video.set(4, 960)

    # Initialize a resizable window.
    cv2.namedWindow('Pose Classification', cv2.WINDOW_NORMAL)

    # Iterate until the webcam is accessed successfully.
    while camera_video.isOpened():

        # Read a frame.
        ok, frame = camera_video.read()

        # Check if frame is not read properly.
        if not ok:
            # Continue to the next iteration to read the next frame and ignore the empty camera frame.
            continue

        # Flip the frame horizontally for natural (selfie-view) visualization.
        frame = cv2.flip(frame, 1)

        # Get the width and height of the frame
        frame_height, frame_width, _ = frame.shape

        # Resize the frame while keeping the aspect ratio.
        frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))

        # Perform Pose landmark detection.
        frame, landmarks = detectPose(frame, pose_video, display=False)

        # Check if the landmarks are detected.
        if landmarks:
            # Perform the Pose Classification.
            frame, _ = classifyPose(landmarks, frame, display=False)

        # Display the frame.
        cv2.imshow('Pose Classification', frame)

        # Wait until a key is pressed.
        # Retreive the ASCII code of the key pressed
        k = cv2.waitKey(1) & 0xFF

        # Check if 'ESC' is pressed.
        if (k == 27):
            # Break the loop.
            break

    # Release the VideoCapture object and close the windows.
    camera_video.release()
    cv2.destroyAllWindows()
#######nomove###########nomove###############nomove###############nomove###############nomove#############nomove###############nomove##############nomove###################
#######nomove###########nomove###############nomove###############nomove###############nomove#############nomove###############nomove##############nomove###################
#######nomove###########nomove###############nomove###############nomove###############nomove#############nomove###############nomove##############nomove###################

####situp#########situp###########situp############situp############situp############situp####situp#####situp##############situp##########situp#############
####situp#########situp###########situp############situp############situp############situp####situp#####situp##############situp##########situp#############
####situp#########situp###########situp############situp############situp############situp####situp#####situp##############situp##########situp#############
def situpcmd():
    import cv2
    import mediapipe as mp
    import numpy as np

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose


    def calculate_angle(a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle


    cap = cv2.VideoCapture(Q,cv2.CAP_DSHOW)
    cv2.namedWindow('Mediapipe Feed', cv2.WINDOW_NORMAL)

    # Curl counter variables
    counter = 0
    stage = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                # Calculate angle
                left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
                right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                if left_hip_angle > 180:
                    left_hip_angle = 360 - left_hip_angle
                if right_hip_angle > 180:
                    right_hip_angle = 360 - right_hip_angle
                if right_knee_angle > 180:
                    right_knee_angle = 360 - right_knee_angle
                if left_knee_angle > 180:
                    left_knee_angle = 360 - left_knee_angle

                try:
                    Calories = counter * kg /100
                except:
                    Calories = counter * 0.48

                # Curl counter logic
                if ((right_knee_angle and left_knee_angle) < 90):
                    if ((left_hip_angle and right_hip_angle) > 85):
                        stage = "up"
                    if ((left_hip_angle and right_hip_angle) < 30) and stage == 'up':
                        stage = "down"
                        counter += 1
                        print(counter)
                        ''''
                if (angle-right_angle>30) or (right_angle-angle>30):
                    cv2.putText(image, 'Very dangerous', (image_height+20,image_width-12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)
    '''

            except:
                pass

            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0, 0), (400, 73), (245, 117, 16), -1)

            # Rep data
            cv2.putText(image, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (65, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, stage,
                        (60, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            try:
                calories = counter * kg  /150
            except:
                calories = counter * 47 / 100
            cv2.putText(image, 'Calories', (250, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(calories),
                        (245, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.rectangle
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            cv2.imshow('Mediapipe Feed', image)

            k = cv2.waitKey(1) & 0xFF

            # Check if 'ESC' is pressed.
            if (k == 27):
                # Break the loop.
                break

        cap.release()
        cv2.destroyAllWindows()

########situp########situp###############situp############situp##########situp###########situp#########situp####situp#######situp##############situp###################
########situp########situp###############situp############situp##########situp###########situp#########situp####situp#######situp##############situp###################
########situp########situp###############situp############situp##########situp###########situp#########situp####situp#######situp##############situp###################

#########ling##########ling##########ling##############ling###########ling############ling###########ling##########ling#####################
#########ling##########ling##########ling##############ling###########ling############ling###########ling##########ling#####################
#########ling##########ling##########ling##############ling###########ling############ling###########ling##########ling#####################
def Alin():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    def calculate_angle(a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    cap = cv2.VideoCapture(Q,cv2.CAP_DSHOW)
    cv2.namedWindow('Mediapipe Feed', cv2.WINDOW_NORMAL)

    # Curl counter variables
    counter = 0
    stage = None
    left_stage = None
    right_stage = None
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculate angle
                left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Visualize angle
                '''
                cv2.putText(image, str(left_angle), 
                               tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                '''
                # Curl counter logic
                if left_angle > 160:
                    left_stage = "down"
                if left_angle < 30 and left_stage == 'down':
                    left_stage = "up"
                    counter += 1
                    print(counter)

                if right_angle > 160:
                    right_stage = "down"
                if right_angle < 30 and right_stage == 'down':
                    right_stage = "up"
                    counter += 1
                    print(counter)

            except:
                pass

            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0, 0), (270, 73), (245, 117, 16), -1)

            # Rep data
            cv2.putText(image, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (90, 12),
                        cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, left_stage,
                        (90, 60),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, right_stage,
                        (180, 60),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            cv2.imshow('Mediapipe Feed', image)

            k = cv2.waitKey(1) & 0xFF

            # Check if 'ESC' is pressed.
            if (k == 27):
                # Break the loop.
                break

        cap.release()
        cv2.destroyAllWindows()
######ling##########ling#######################ling#################lingling########################ling#####ling####
######ling##########ling#######################ling#################lingling########################ling#####ling####
######ling##########ling#######################ling#################lingling########################ling#####ling####

########push#################push##################push################push###########push################push#############push########
########push#################push##################push################push###########push################push#############push########
########push#################push##################push################push###########push################push#############push########
def pup():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    def calculate_angle(a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    cap = cv2.VideoCapture(Q,cv2.CAP_DSHOW)
    cv2.namedWindow('Mediapipe Feed', cv2.WINDOW_NORMAL)

    # Curl counter variables
    counter = 0
    stage = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            #image_height, image_width, _ = image
            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            try:
                image_height,image_width,_ = image
            except:
                pass

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                rightshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                rightelbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rightwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculate angle
                angle = calculate_angle(shoulder, elbow, wrist)
                right_angle = calculate_angle(rightshoulder, rightelbow, rightwrist)

                # Visualize angle
                '''
                cv2.putText(image, str(int(angle)), 
                               tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                cv2.putText(image, str(int(right_angle)), 
                               tuple(np.multiply(rightelbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
            '''

                # Curl counter logic
                if ((right_angle) > 145):
                    stage = "down"
                if ((right_angle) < 115) and stage == 'down':
                    stage = "up"
                    counter += 1
                    print(counter)
                if (angle - right_angle > 30) or (right_angle - angle > 30):
                    cv2.putText(image, 'Very dangerous', (image_height + 20, image_width - 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

            except:
                pass


            try:
                calories = counter * kg /200
            except:
                calories = counter * 57 / 200
            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0, 0), (400, 73), (245, 117, 16), -1)

            # Rep data
            cv2.putText(image, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (65, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, stage,
                        (60, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # calories
            # ---------------------------------------------------------------------------#

            try:
                calories = counter * kg / 200
            except:
                calories = counter * 57 / 200
            cv2.putText(image, 'Calories', (250, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(calories),
                        (245, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            # ----------------------------------------------------------------------------#
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            cv2.imshow('Mediapipe Feed', image)

            k = cv2.waitKey(1) & 0xFF

            # Check if 'ESC' is pressed.
            if (k == 27):
                # Break the loop.
                break

        cap.release()
        cv2.destroyAllWindows()


######push######push######push######push######push######push######push######push######push######push######push######push
######push######push######push######push######push######push######push######push######push######push######push######push
######push######push######push######push######push######push######push######push######push######push######push######push


######squart###########squart################squart###############squart############squart###########squart##########squart######squart#################
######squart###########squart################squart###############squart############squart###########squart##########squart######squart#################
######squart###########squart################squart###############squart############squart###########squart##########squart######squart#################
def square():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    def calculate_angle(a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    cap = cv2.VideoCapture(Q,cv2.CAP_DSHOW)
    cv2.namedWindow('Mediapipe Feed', cv2.WINDOW_NORMAL)
    # Curl counter variables
    counter = 0
    stage = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            #image_height, image_width, _ = image
            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                # Calculate angle
                left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
                right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                if left_hip_angle > 180:
                    left_hip_angle = 360 - left_hip_angle
                if right_hip_angle > 180:
                    right_hip_angle = 360 - right_hip_angle
                if right_knee_angle > 180:
                    right_knee_angle = 360 - right_knee_angle
                if left_knee_angle > 180:
                    left_knee_angle = 360 - left_knee_angle

                # Curl counter logic
                if ((left_hip_angle and right_hip_angle and right_knee_angle and left_knee_angle) > 160):
                    stage = "down"
                if ((
                            left_hip_angle and right_hip_angle and right_knee_angle and left_knee_angle) < 110) and stage == 'down':
                    if ((left_hip_angle and right_hip_angle and right_knee_angle and left_knee_angle) > 75):
                        stage = "up"
                        counter += 1
                        print(counter)
                        ''''
                if (angle-right_angle>30) or (right_angle-angle>30):
                    cv2.putText(image, 'Very dangerous', (image_height+20,image_width-12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)
    '''

            except:
                pass

            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0, 0), (400, 73), (245, 117, 16), -1)

            # Rep data
            cv2.putText(image, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(image, 'STAGE', (65, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, stage,
                        (60, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # calories
            # ---------------------------------------------------------------------------#
            try:
                calories = 3.5 * kg / 400 *counter
            except:
                calories = counter * 8 / 25
            cv2.putText(image, 'Calories', (250, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(calories),
                        (245, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            # ----------------------------------------------------------------------------#

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            cv2.imshow('Mediapipe Feed', image)

            k = cv2.waitKey(1) & 0xFF

            # Check if 'ESC' is pressed.
            if (k == 27):
                # Break the loop.
                break

        cap.release()
        cv2.destroyAllWindows()
#################squart#################squart#################squart#################squart#################squart#################squart##########
#################squart#################squart#################squart#################squart#################squart#################squart##########
#################squart#################squart#################squart#################squart#################squart#################squart##########
print("Input Age, gender, height and weight")
########################
def elvisugly():
    print("Elive Ugly")


age_lb = Label(frame, text="Enter Age (2 - 120)")
age_lb.grid(row=1, column=1)
age_lb.bind("<Key>", labeler)
age_tf = Entry(frame)
age_tf.grid(row=1, column=2, pady=5)

gen_lb = Label(frame, text='Select Gender')
gen_lb.grid(row=2, column=1)

frame2 = Frame(frame)
frame2.grid(row=2, column=2, pady=5)

male_rb = Radiobutton(frame2, text='Male', variable=var, value=1)
male_rb.pack(side=LEFT)

female_rb = Radiobutton(frame2, text='Female', variable=var, value=2)
female_rb.pack(side=RIGHT)

height_lb = Label(frame, text="Enter Height (cm)  ")
height_lb.grid(row=3, column=1)

weight_lb = Label(frame, text="Enter Weight (kg)  ")
weight_lb.grid(row=4, column=1)

height_tf = Entry(frame)
height_tf.grid(row=3, column=2, pady=5)

weight_tf = Entry(frame)
weight_tf.grid(row=4, column=2, pady=5)

frame3 = Frame(frame)
frame3.grid(row=5, columnspan=3, pady=10)

cal_btn = Button(frame3, text='Calculate', command=calculate_bmi)
cal_btn.pack(side=LEFT)

reset_btn = Button(frame3, text='Reset', command=reset_entry)
reset_btn.pack(side=LEFT)

continue_btn = Button(frame3, text='Continue', command=lambda: root.destroy())
continue_btn.pack(side=RIGHT)

# btn1 = tk.Button(win1, text="Click to open a new window", command=btn1_clicked)
label = weight_lb = Label(frame, text="PS:切勿填寫假資料，將會導致數據計算錯誤")
label.grid(row=9, column=2, pady=20)

root.mainloop()


from tkinter import *
from tkinter import messagebox

try:
    import Tkinter as tk
except:
    import tkinter as tk

choose = Tk()
choose.configure(bg="purple")

choose.geometry('400x400')

var = IntVar()

chooseme = Frame(choose, padx=10, pady=10, bg="orange")
chooseme.pack(expand=True)


squart_btn = Button(chooseme, text="Squart",command = square)
squart_btn.grid(row=1, column=1)
situp_btn = Button(chooseme, text="Sit up", command =situpcmd)
situp_btn.grid(row=2, column=1)
pushup_btn = Button(chooseme, text="Push up",command  = pup)
pushup_btn.grid(row=3, column=1)
aling_btn = Button(chooseme, text="Dumbbell",command=Alin)
aling_btn.grid(row=4, column=1)
others_btn = Button(chooseme, text="Others move", command=nomove)
others_btn.grid(row=5, column=1)
continue_btn = Button(chooseme, text='quit', command=elvisugly)
continue_btn.grid(row=6, column=1)

chooseme.mainloop()
