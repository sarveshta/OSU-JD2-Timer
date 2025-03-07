from inference import get_model
import supervision as sv
import cv2

# load the pre-trained YOLO model using the coco-dataset-vdnr1/23 model
model = get_model(model_id="coco-dataset-vdnr1/23")

# create supervision annotators for bounding boxes and labels
bounding_box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# open the default camera (use the appropriate camera index if needed)
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # run inference on the current frame
    results = model.infer(frame)[0]

    # load inference results into the Supervision Detections API
    detections = sv.Detections.from_inference(results)

    # annotate the frame with bounding boxes and labels
    annotated_frame = bounding_box_annotator.annotate(scene=frame, detections=detections)
    annotated_frame = label_annotator.annotate(scene=annotated_frame, detections=detections)

    # display the annotated frame in a window named "Camera Inference"
    cv2.imshow("Camera Inference", annotated_frame)

    # exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the camera and close any open windows
cap.release()
cv2.destroyAllWindows()
