import cv2
import numpy as np

# Load the image
image = cv2.imread("drawing.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Preprocessing
blur = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    # Approximate the contour
    approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
    x, y, w, h = cv2.boundingRect(approx)

    # Identify shape based on number of sides
    if len(approx) == 3:
        shape = "Triangle"
    elif len(approx) == 4:
        # Check aspect ratio to distinguish square vs rectangle
        aspect_ratio = float(w) / h
        shape = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
    elif len(approx) == 5:
        shape = "Pentagon"
    elif len(approx) > 6:
        shape = "Circle"
    else:
        shape = "Polygon"

    # Draw contour and label
    cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)
    cv2.putText(image, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

cv2.imshow("Detected Shapes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()