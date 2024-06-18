import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import io
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# Hide the main tkinter window
Tk().withdraw()

# Open file dialog and select the image
file_path = askopenfilename(title="Select an image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])

if not file_path:
    print("No file selected")
    exit()

# Load the image
image = io.imread(file_path)

# Compute histogram
occurrences, bins = np.histogram(image, bins=256, range=(0, 255))

# Sort histogram occurrences in descending order
sorted_occurrences = np.sort(occurrences)[::-1]
idx = np.argsort(occurrences)[::-1]

# Calculate the cumulative sum
cumulative_sum = np.cumsum(sorted_occurrences)

# Find the threshold index
threshold_index = np.where(cumulative_sum >= 0.99 * np.sum(occurrences))[0][0]

# Select the top 90% most occurred intensities
selected_bins = bins[idx[:threshold_index]]
selected_occurrences = sorted_occurrences[:threshold_index]

# Create a copy of the original image
modified_image = np.copy(image)

# Initialize a logical mask
mask = np.zeros(image.shape, dtype=bool)

# Find the indices of pixels whose bins were removed
for i in range(len(bins)-1):
    if bins[i] not in selected_bins:
        mask |= (image == bins[i])

# Set the pixel values at removed indices to zero
modified_image[mask] = 0

# Plot original image and histogram
plt.figure(figsize=(10, 8))

# Original Image
plt.subplot(2, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

# Original Histogram
plt.subplot(2, 2, 2)
plt.bar(bins[:-1], occurrences, width=1)
plt.title('Original Histogram')
plt.xlabel('Intensity')
plt.ylabel('Occurrences')
plt.xlim([0, 255])

# Modified Image
plt.subplot(2, 2, 3)
plt.imshow(modified_image, cmap='gray')
plt.title('Modified Image')
plt.axis('off')

# Modified Histogram
plt.subplot(2, 2, 4)
plt.bar(selected_bins, selected_occurrences, width=1)
plt.title('Modified Histogram (90% most occurred intensities)')
plt.xlabel('Intensity')
plt.ylabel('Occurrences')
plt.xlim([0, 255])

plt.tight_layout()
plt.show()
