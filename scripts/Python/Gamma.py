from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
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
image = Image.open(file_path).convert('L')  

# Adjust the image contrast
# Convert to grayscale if needed
enhancer = ImageEnhance.Contrast(image)
J = enhancer.enhance(2)

# Display the original and adjusted images side by side
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].imshow(np.asarray(image), cmap='gray')
axs[0].set_title('Original Image')
axs[0].axis('off')

axs[1].imshow(np.asarray(J), cmap='gray')
axs[1].set_title('Adjusted Image')
axs[1].axis('off')

plt.show()
