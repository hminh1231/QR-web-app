import streamlit as st 
import pandas as pd
import numpy as np
import qrcode
import cv2
from PIL import Image



# streamlit_app.py
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
            
            
        data = {'Project': [project], 'Boring No.': [boring], 'Sample No.': [sample],'	Depth (m)': [depth],'Bag /Tube': [bag],'Test Name': [testname],'Remarks': [remarks] }
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
    st.title("Generate QR Code")

    # Tạo các widgets để nhập thông tin
    project = st.text_input("Input Project:")
    boring = st.text_input("Input Boring No.:")
    sample = st.text_input("Input Sample No.:")
    depth = st.text_input("Input Depth (m):")
    bag = st.text_input("Input Bag /Tube:")
    testname = st.text_input("Input Test Name:")
    remarks = st.text_input("Input Remarks:")
    
    
    
    # Khi người dùng nhấn nút "Lưu"
    if st.button("Save"):
        img_file = st.empty()
        # Format data string with delimiters
        data = f"{project}|{boring}|{sample}|{depth}|{bag}|{testname}|{remarks}"

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
        qr_img.save("product_qr.png")

        st.image('product_qr.png')
        
        
        # Tạo DataFrame từ thông tin người dùng
        data = {'Project': [project], 'Boring No.': [boring], 'Sample No.': [sample],'	Depth (m)': [depth],'Bag /Tube': [bag],'Test Name': [testname],'Remarks': [remarks] }
        #Project	Boring No.	Sample No. 	Depth (m)	"Bag /Tube"	Test Name	Remarks

        
        df = pd.DataFrame(data)

        # Lưu vào tệp Excel
        output = df.to_excel('data.xlsx', index=False)
        

        # Hiển thị thông tin vừa lưu lên giao diện
        st.write("Information have been saved:")
        st.write(df)
        
        with open('data.xlsx', 'rb') as file:
            file_data = file.read()
        
        st.download_button(
            label="Click here to download Excel",
            data=file_data,
            key="excel-download",
            file_name="data.xlsx",
        )
    if st.button("clear data"):
        data = {'Project': [], 'Boring No.': [], 'Sample No.': [],'	Depth (m)': [],'Bag /Tube': [],'Test Name': [],'Remarks': [] }
        df = pd.DataFrame(data)

        # Lưu vào tệp Excel
        output = df.to_excel('data.xlsx', index=False)
        # Hiển thị thông tin vừa lưu lên giao diện
        st.write("Information have been deleted:")
        st.write(df)
        

