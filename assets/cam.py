import cv2
import pytesseract
from googletrans import Translator

# Initialize translator
translator = Translator()

# Configure Tesseract OCR (set the path if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Change this path if necessary

def capture_and_translate():
    cap = cv2.VideoCapture(0)  # Open the camera

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Show the camera feed
        cv2.imshow("Camera - Press 's' to scan", frame)

        # Press 's' to scan and translate text
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite("captured_text.jpg", frame)
            print("Image captured! Extracting text...")

            # Convert image to grayscale for better OCR results
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)

            if text.strip():
                print(f"Extracted Text: {text}")
                
                # Translate to English
                translated_text = translator.translate(text, dest="en").text
                print(f"Translated Text: {translated_text}")
            else:
                print("No text detected!")

        elif key == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the translation function
capture_and_translate()