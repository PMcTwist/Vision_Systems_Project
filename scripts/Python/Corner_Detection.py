import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
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
image = cv2.imread(file_path)  # Replace 'cameraman.jpg' with your image file

# Convert the image to grayscale if it is not already
if len(image.shape) == 3:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
else:
    gray_image = image

# Compute the image gradients
Ix = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
Iy = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

# Compute products of derivatives at every pixel
Ix2 = Ix**2
Iy2 = Iy**2
Ixy = Ix * Iy

# Apply Gaussian smoothing to the derivative products
Sxx = gaussian_filter(Ix2, sigma=2)
Syy = gaussian_filter(Iy2, sigma=2)
Sxy = gaussian_filter(Ixy, sigma=2)

# Set the sensitivity factor and threshold
k = 0.04  # Sensitivity factor
threshold = 1e6  # Threshold for detecting corners

# Compute the Harris response for each pixel
R = (Sxx * Syy - Sxy**2) - k * (Sxx + Syy)**2

# Find corners where R is above the threshold
corners = R > threshold

# Perform non-maximum suppression
local_max = (R == cv2.dilate(R, None))
harris_corners = corners & local_max

# Display the results
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.scatter(np.where(harris_corners)[1], np.where(harris_corners)[0], c='r', s=5)
plt.show()
