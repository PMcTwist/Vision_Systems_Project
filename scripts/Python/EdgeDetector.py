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

# Read the image
image = cv2.imread(file_path)

# Convert to grayscale if necessary
if len(image.shape) == 3:
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
else:
    image_gray = image

# Step 1: Noise Reduction (Gaussian Blur)
blurred = cv2.GaussianBlur(image_gray, (5, 5), 1)

# Step 2: Gradient Calculation (Sobel Operator)
gradient_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
gradient_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
magnitude = np.sqrt(gradient_x**2 + gradient_y**2)

# Step 3: Non-maximum Suppression
angle = np.rad2deg(np.arctan2(gradient_y, gradient_x))
angle[angle < 0] += 180

suppressed = np.copy(magnitude)
rows, cols = suppressed.shape

for i in range(1, rows-1):
    for j in range(1, cols-1):
        try:
            q = 255
            r = 255

            # angle 0
            if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                q = magnitude[i, j+1]
                r = magnitude[i, j-1]
            # angle 45
            elif (22.5 <= angle[i,j] < 67.5):
                q = magnitude[i+1, j-1]
                r = magnitude[i-1, j+1]
            # angle 90
            elif (67.5 <= angle[i,j] < 112.5):
                q = magnitude[i+1, j]
                r = magnitude[i-1, j]
            # angle 135
            elif (112.5 <= angle[i,j] < 157.5):
                q = magnitude[i-1, j-1]
                r = magnitude[i+1, j+1]

            if (magnitude[i,j] < q) or (magnitude[i,j] < r):
                suppressed[i,j] = 0

        except IndexError as e:
            pass

# Step 4: Double Thresholding
low_threshold = 30
high_threshold = 100
strong_edges = (suppressed > high_threshold).astype(np.uint8)
weak_edges = ((suppressed >= low_threshold) & (suppressed <= high_threshold)).astype(np.uint8)

# Step 5: Edge Tracking by Hysteresis
edges = np.copy(strong_edges)
for i in range(1, rows-1):
    for j in range(1, cols-1):
        if weak_edges[i, j]:
            if np.any(strong_edges[i-1:i+2, j-1:j+2]):
                edges[i, j] = 1

edges = (edges * 255).astype(np.uint8)

# Display the images
plt.figure(figsize=(12, 8))

plt.subplot(2, 3, 1)
plt.imshow(image_gray, cmap='gray')
plt.title('Original Image')

plt.subplot(2, 3, 2)
plt.imshow(blurred, cmap='gray')
plt.title('Blurred Image')

plt.subplot(2, 3, 3)
plt.imshow(magnitude, cmap='gray')
plt.title('Gradient Magnitude')

plt.subplot(2, 3, 4)
plt.imshow(suppressed, cmap='gray')
plt.title('Non-maximum Suppression')

plt.subplot(2, 3, 5)
plt.imshow(strong_edges, cmap='gray')
plt.title('Strong Edges')

plt.subplot(2, 3, 6)
plt.imshow(edges, cmap='gray')
plt.title('Final Edges')

plt.tight_layout()
plt.show()
