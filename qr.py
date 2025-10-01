import qrcode

# Data you want to encode
data = "https://www.example.com"

# Create QR code
qr = qrcode.QRCode(
    version=1,  # controls the size of the QR code (1 = smallest)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # error correction level
    box_size=10,  # size of each box in pixels
    border=4,  # border size (minimum is 4)
)

qr.add_data(data)
qr.make(fit=True)

# Create an image
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
img.save("qrcode.png")

print("QR Code generated and saved as qrcode.png")