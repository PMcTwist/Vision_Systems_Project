import cv2
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

# Read the image - Default BGR Format
image = cv2.imread(file_path)
# Convert BGR to RGB for correct color display with matplotlib
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  

# Split the image into its RGB components
redChannel = image[:, :, 0]
greenChannel = image[:, :, 1]
blueChannel = image[:, :, 2]

# Save each component as a separate image
cv2.imwrite('red_component.jpg', redChannel)
cv2.imwrite('green_component.jpg', greenChannel)
cv2.imwrite('blue_component.jpg', blueChannel)

# Plot the images
plt.subplot(2, 2, 1)
plt.imshow(image)
plt.title('Original Image')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(redChannel)
plt.title('Red Component')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(greenChannel)
plt.title('Green Component')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.imshow(blueChannel)
plt.title('Blue Component')
plt.axis('off')

plt.show()
