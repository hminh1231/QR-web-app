import streamlit as st 
import pandas as pd
import numpy as np
from utils import create_zip, generate_qr_code, get_image_list
import cv2
from PIL import Image
import os

st.header("QR Scan & Generate application")
def check_password():
    """Returns `True` if the user had a correct password."""
    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] == 'admin' and st.session_state["password"] == 'admin':
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False

if not check_password():
    st.stop()

# Tạo một session state để theo dõi trạng thái của trang
session_state = st.session_state

# Trang chính
if 'page' not in session_state:
    session_state.page = "Home"

# Menu chọn trang
page = st.selectbox("Select Pages:", ["Home", "Generate QR Code", "Extract QR Code"])

# Lưu trạng thái trang vào session state
session_state.page = page
# Trang chuyển đổi
if session_state.page == "Extract QR Code":
    st.title("Extract QR Information")
    picture = st.camera_input("Take a picture")

    if picture:
        st.image(picture)
        # Load image
        img = Image.open(picture)
        # To convert PIL Image to numpy array:
        img_array = np.array(img)
        # Detect and decode
        detector = cv2.QRCodeDetector()
        data, bbox, rectified_img = detector.detectAndDecode(img_array)
        st.text("Data extracted: ")
        try:
            project, boring,sample, depth, bag,testname, remarks =  data.split("|")
        # Tạo DataFrame từ thông tin người dùng
        except:
            project = data
            boring = data
            sample = data
            depth = data
            bag = data
            testname = data
            remarks = data
            
            
        data = {'Project': [project], 'Boring No.': [boring], 'Sample No.': [sample],'Depth (m)': [depth],'Bag /Tube': [bag],'Test Name': [testname],'Remarks': [remarks] }
        df_extract = pd.DataFrame(data)
        output = df_extract.to_excel('data_extracted.xlsx', index=False)
        st.write("Information have been extracted:")
        st.write(df_extract)
        
        with open('data_extracted.xlsx', 'rb') as file:
            file_data = file.read()
        
        st.download_button(
            label="Click here to download Excel",
            data=file_data,
            key="excel-download",
            file_name="data_extracted.xlsx",
        )

elif session_state.page == "Generate QR Code":
    # Initialize the DataFrame if it doesn't exist or read it from the file
    try:
        df = pd.read_excel('data.xlsx')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Project', 'Boring No.', 'Sample No.', 'Depth (m)', 'Bag /Tube', 'Test Name', 'Remarks'])

    st.title("Generate QR Code")
    
    # Tạo các widgets để nhập thông tin
    project = st.text_input("Input Project:")
    boring = st.text_input("Input Boring No.:")
    sample = st.text_input("Input Sample No.:")
    depth = st.text_input("Input Depth (m):")
    bag = st.text_input("Input Bag /Tube:")
    testname = st.text_input("Input Test Name:")
    remarks = st.text_input("Input Remarks:")
    save_btn = st.button("Save")
    
    placeholder_result = st.empty()
    with placeholder_result.container():
        st.write("Table QR information:")
        st.dataframe(df, use_container_width=True)
    # When the user clicks "Save"
    if save_btn:
        # Format data string with delimiters
        data = f"{project}|{boring}|{sample}|{depth}|{bag}|{testname}|{remarks}"
        idx_img = len(df['Project'].values)
        # Generate a QR code
        img_or_path = f'./img_qr/product_qr_{idx_img}.png'
        qr_img = generate_qr_code(data, img_or_path)

        # Display the QR code
        st.image(img_or_path)

        # Append the data to the DataFrame
        new_row = {
            'Project': project,
            'Boring No.': boring,
            'Sample No.': sample,
            'Depth (m)': depth,
            'Bag /Tube': bag,
            'Test Name': testname,
            'Remarks': remarks
        }
        df = df._append(new_row, ignore_index=True)

        # Save the updated DataFrame to the Excel file
        df.to_excel('data.xlsx', index=False)
        
        # Display the information saved
        with placeholder_result.container():
            st.text("Information have been saved:")
            st.dataframe(df, use_container_width=True)
        #st.write(df)
    

    try:
        df = pd.read_excel('data.xlsx')
        with open('data.xlsx', 'rb') as file:
            file_data = file.read()
      
            st.download_button(
                label="Click here to download Excel",
                data=file_data,
                key="excel-download",
                file_name="data_extracted.xlsx",
            )
        
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Project', 'Boring No.', 'Sample No.', 'Depth (m)', 'Bag /Tube', 'Test Name', 'Remarks'])
        df.to_excel('data.xlsx')
        with open('data.xlsx', 'rb') as file:
            file_data = file.read()
    
    
    image_list = get_image_list('./img_qr')
    zip_filename = 'images.zip'
    create_zip(image_list, zip_filename)

    with open(zip_filename, "rb") as f:
        zip_data = f.read()
        
        st.download_button(
        label="Click here to download ZIP Images QR",
        data=zip_data,
        key="zip-download",
        file_name="images.zip",
        )
        
        # When the user clicks "Clear Data"
    
    if st.button("Clear Data"):
        # Clear the DataFrame
        df = pd.DataFrame(columns=['Project', 'Boring No.', 'Sample No.', 'Depth (m)', 'Bag /Tube', 'Test Name', 'Remarks'])
        # Save the cleared DataFrame to the Excel file
        df.to_excel('data.xlsx', index=False)
        # Display a message indicating data has been cleared
        #with result_table:
        image_list_path = os.listdir('./img_qr')
        for img_path in image_list_path:
            if os.path.exists('./img_qr/'+img_path):
                os.remove('./img_qr/'+img_path)
        
        with placeholder_result.container():
            st.write("Information have been cleared:")
            st.dataframe(df, use_container_width=True)
            #st.write(df)