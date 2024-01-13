import qrcode
import zipfile
import os

# Function to get the list of image files in a folder
def get_image_list(folder_path):
    image_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image_list.append(os.path.join(folder_path, filename))
    return image_list

# Function to create a ZIP file from a list of files
def create_zip(image_list, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for image_path in image_list:
            zipf.write(image_path, os.path.basename(image_path))

# Function to create a QR code
def generate_qr_code(data, path):
# Generate a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code as an image
    qr_img.save(path)

    return qr_img