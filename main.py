import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from gtts import gTTS
from playsound import playsound
from food_facts import food_facts

def speech(text):
    print(text)
    language = "en"
    output = gTTS(text=text, lang=language, slow=False)

    output.save("./sounds/output.mp3")
    playsound("./sounds/output.mp3")
    
    bbox, label, conf = cv.detect_common_objects(frame, confidence=0.5, resize=(800, 600))


video = cv2.VideoCapture(0)  # Use index 0 for the default camera

if not video.isOpened():  # Check if camera access failed
    print("Error: Unable to access the camera.")
    exit()

labels = []

while True:
    ret, frame = video.read()
    
    if not ret:  # Check if frame reading failed
        print("Error: Unable to capture frame from the camera.")
        break

    bbox, label, conf = cv.detect_common_objects(frame)

    output_image = draw_bbox(frame, bbox, label, conf)

    cv2.imshow("Detection", output_image)

    for item in label:
        if item not in labels:
            labels.append(item)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

if labels:
    i = 0
    new_sentence = []
    for label in labels:
        if i == 0:
            new_sentence.append(f"I found a {label}, and, ")
        else:
            new_sentence.append(f"a {label},")
        i += 1

    speech(" ".join(new_sentence))
    speech("Here are the food facts I found for these items:")

    for label in labels:
        try:
            print(f"\n\t{label.title()}")
            food_facts(label)
        except:
            print("No food facts for this item")
else:
    print("No objects detected.")

video.release()
cv2.destroyAllWindows()

