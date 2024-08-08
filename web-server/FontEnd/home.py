import streamlit as st


class Home:
    def __init__(self) -> None:
        self.link_image1 = 'none'
        self.link_image2 = 'none'
    
    def app(self):
        st.subheader('Hệ thống giám sát môi trường', divider='rainbow')
        st.subheader('_Giới thiệu_')
        colum1, colum2 = st.columns(2)
        with colum1:
            st.write("Hệ thống giám sát môi trường là hệ thống giám sát môi trường trực tuyến.")
            st.write("Hệ thống giám sát môi trường sử dụng các cảm biến để đo lường các thông số môi trường như nhiệt độ, độ ẩm, khí CO, PM 1, PM 2.5, PM 10.")
            st.image(self.getImage1(), width=450)

        with colum2:
            st.write("Hệ thống giám sát môi trường cung cấp thông tin về môi trường xung quanh.")
            st.write("Hệ thống này có thể được kết hợp với các phần mềm và ứng dụng điều khiển thông minh, cho phép người dùng theo dõi và điều kiển đèn từ xa thông qua web app")
            st.image(self.getImage2(), width=450)

    def setImage1(self, link):
        self.link_image1 = link

    def setImage2(self, link):
        self.link_image2 = link

    def getImage1(self):
        return self.link_image1
    
    def getImage2(self):
        return self.link_image2

    

