import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# Hide the main tkinter window
Tk().withdraw()

# Open file dialog and select the image
file_path = askopenfilename(title="Select an image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])

if not file_path:
    print("No file selected")
    exit()

# Read grayscale image
image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

# Calculate histogram
histogram = cv2.calcHist([image], [0], None, [256], [0, 256])

# Calculate normalized histogram
num_pixels = image.size
normalized_histogram = histogram / num_pixels

# Display original image
plt.subplot(2, 1, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')

# Display histogram
plt.subplot(2, 2, 3)
plt.bar(range(256), histogram[:, 0])
plt.title('Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

# Display normalized histogram
plt.subplot(2, 2, 4)
plt.bar(range(256), normalized_histogram[:, 0])
plt.title('Normalized Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Normalized Frequency')

plt.tight_layout()
plt.show()
