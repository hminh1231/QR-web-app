import streamlit as st
import os
import zipfile

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

# Streamlit app
def main():
    st.title("Image Downloader App")

    # Sidebar to input folder path
    folder_path = st.sidebar.text_input("Enter folder path containing images:")

    if folder_path:
        image_list = get_image_list(folder_path)

        if image_list:
            st.write(f"Found {len(image_list)} image(s) in the folder:")
            for image_path in image_list:
                st.image(image_path, use_column_width=True)

            # Button to download images
            if st.button("Download Images as ZIP"):
                zip_filename = 'images.zip'
                create_zip(image_list, zip_filename)

                with open(zip_filename, "rb") as f:
                    zip_data = f.read()
                st.download_button(
                    label="Click here to download ZIP",
                    data=zip_data,
                    key="zip-download",
                    file_name="images.zip",
                )
        else:
            st.warning("No images found in the specified folder.")
    else:
        st.warning("Please enter a folder path.")

if __name__ == "__main__":
    main()
