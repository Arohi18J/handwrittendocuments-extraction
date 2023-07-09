from tkinter import *
from tkinter import filedialog
import fpdf
import cv2
import pytesseract as tess
import numpy as np
from PIL import Image
from difflib import SequenceMatcher

tess.pytesseract.tesseract_cmd = r'C:\Users\Prathamesh\Desktop\ocrproject1\Handwritten_Text_Recognition-main\Tesseract-OCR'

result = None  # Initialize result variable

def browseFiles():
    global result
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                          filetypes=(("images", "*.png *.jpg *jpeg"), ("all files", "*.*")))
    if filename == "":
        return

    try:
        # Read image with OpenCV
        img = cv2.imread(filename)

        # Convert to gray
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply dilation and erosion to remove noise
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        # Write image after noise removal
        cv2.imwrite("removed_noise.png", img)

        # Apply threshold to get black and white image
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Write the processed image
        cv2.imwrite(filename, img)

        # Recognize text with Tesseract
        result = tess.image_to_string(Image.open(filename))

        # Update label with the result
        label_file_explorer.configure(text=result)

    except Exception as e:
        print("Error:", str(e))
        result = None

def pdf():
    global result
    if result is not None:
        pdf = fpdf.FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.write(5, result)
        pdf.ln()
        pdf.output("converted.pdf")

window = Tk()
window.title('File Explorer')
window.geometry("700x350")

reg_info = Label(window, text="Handwritten Text Recognition Using Pytesseract",
                 width='80', height='2', font=("ariel", 12, "bold"), fg="black", bg='lightgrey')
reg_info.place(x=370, y=18, anchor='center')

window.config(background="white")

label_file_explorer = Label(window, text="See the Output Here", font=("ariel", 10, "bold"),
                            width=90, height=12, fg="blue")
label_file_explorer.place(x=0, y=35)

button_explore = Button(window, text="Browse Files", fg="white", bg="black",
                        font=("ariel", 10, "bold"), width=10, command=browseFiles)
button_explore.place(x=250, y=270)

text = Label(window, text="(Select an image)", bg="white", fg="black", font=("ariel", 8, "bold"))
text.place(x=242, y=300)

button1 = Button(window, text="Convert Text to PDF", fg="white", bg="black",
                 font=("ariel", 10, "bold"), width=15, command=pdf)
button1.place(x=370, y=270)

window.mainloop()

if result is not None:
    s = "We start With good\n\nBecause all businesses should\n\nbe doing something good"
    s1 = result

    def similar(a, b):
        return "\nThe accuracy of the model is " + str(SequenceMatcher(None, a, b).ratio() * 100) + "%\n"

    print(similar(s, s1))
