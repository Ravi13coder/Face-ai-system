import cv2
import matplotlib.pyplot as plt

# 1. Load the original image (OpenCV reads as BGR)
img = cv2.imread("image.jpg")   #enter your image name instead of image

# 2. Create an RGB version for correct Matplotlib rendering
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 3. Image Flips
HF_img = cv2.flip(img_rgb, 1)  # Horizontal flip
VF_img = cv2.flip(img_rgb, 0)  # Vertical flip

# 4. Grayscale Conversion
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 5. Channel Manipulations (Using BGR indices: 0=B, 1=G, 2=R)
# Remove Red channel (Sets Red to 0, leaves Blue and Green)
Rred_img = img_rgb.copy()
Rred_img[:, :, 0] = 0  # In RGB, index 0 is Red

# Remove Green channel
Rgreen_img = img_rgb.copy()
Rgreen_img[:, :, 1] = 0  # In RGB, index 1 is Green

# Remove Blue channel
Rblue_img = img_rgb.copy()
Rblue_img[:, :, 2] = 0  # In RGB, index 2 is Blue

# 6. Isolate Blue Channel Only (Zero out Red and Green)
blue_only = img_rgb.copy()
blue_only[:, :, 0] = 0  # Remove Red
blue_only[:, :, 1] = 0  # Remove Green

# 7. Setup Matplotlib Grid (3 rows, 3 columns)
plt.figure(figsize=(12, 10))

# Row 1: Originals and Flips
plt.subplot(3, 3, 1)
plt.imshow(img_rgb)
plt.title("Original Image (RGB)")
plt.axis("off")

plt.subplot(3, 3, 2)
plt.imshow(HF_img)
plt.title("Horizontal Flip")
plt.axis("off")

plt.subplot(3, 3, 3)
plt.imshow(VF_img)
plt.title("Vertical Flip")
plt.axis("off")

# Row 2: Grayscale and Removed Channels
plt.subplot(3, 3, 4)
plt.imshow(gray_image, cmap="gray")
plt.title("Grayscale")
plt.axis("off")

plt.subplot(3, 3, 5)
plt.imshow(Rred_img)
plt.title("Red Removed")
plt.axis("off")

plt.subplot(3, 3, 6)
plt.imshow(Rgreen_img)
plt.title("Green Removed")
plt.axis("off")

# Row 3: Remaining Channels
plt.subplot(3, 3, 7)
plt.imshow(Rblue_img)
plt.title("Blue Removed")
plt.axis("off")

plt.subplot(3, 3, 8)
plt.imshow(blue_only)
plt.title("Only Blue Channel")
plt.axis("off")

# Leaving the 9th subplot empty or reusing grayscale
plt.subplot(3, 3, 9)
plt.imshow(gray_image, cmap="gray")
plt.title("Grayscale (Duplicate)")
plt.axis("off")

plt.tight_layout()
plt.show()
