import cv2

# The image file you loaded
image_path = "./target_image.jpg" 
img = cv2.imread(image_path)

# Bounding Box Coordinates: [x, y, width, height]
bbox = [460, 462, 626, 573]
x, y, w, h = bbox

# Convert to OpenCV's required format: (x1, y1) and (x2, y2)
pt1 = (x, y)              # Top-Left (386, 426)
pt2 = (x + w, y + h)      # Bottom-Right (694, 632)

# Draw the rectangle
# Args: image, pt1, pt2, color (BGR), thickness
color = (255, 255, 255) # Green
thickness = 3
cv2.rectangle(img, pt1, pt2, color, thickness)

# Display the image (optional)
cv2.imshow("Detected Face", img)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the image with the box (optional)
cv2.imwrite("result_with_bbox.jpg", img)