import streamlit as st
from BackEnd.connectSQLite import SQLite

class Account:
    def __init__(self):
        self.data_user = SQLite("BackEnd/data_sql.sqlite")  
        self.username = ""
        self.password = ""

    def app(self):
        if 'check_login' not in st.session_state:
            st.session_state.check_login = False

        st.subheader('Hệ thống giám sát môi trường')
        st.subheader('_Tài khoản người dùng_')

        if st.session_state.check_login:
            st.write("Bạn đã đăng nhập.")
            if st.button("Đăng xuất"):
                st.session_state.check_login = False
                print(f"Logout!")
                print(f"Check login: {st.session_state.check_login}")
                st.rerun()
        else:
            st.write("Bạn chưa đăng nhập. Hãy đăng nhập để sử dụng hệ thống.")
            if st.button("Đăng nhập"):
                self.login()
                
    @st.experimental_dialog("Đăng nhập")
    def login(self):
        with st.form("login_form"):
            username = st.text_input("Tài khoản:")
            password = st.text_input("Mật khẩu:", type="password")
            submit_button = st.form_submit_button("Xong")
            if submit_button:
                print(f"{username} - {password}")
                self.data_user.connectSQL()  
                if self.data_user.isLogin(username, password):
                    st.success("Đăng nhập thành công")
                    st.session_state.check_login = True
                    self.data_user.closeSQL()  
                    print(f"Check login: {st.session_state.check_login}")
                    st.rerun()
                elif not username:
                    st.error("Vui lòng nhập tài khoản")
                elif not password:
                    st.error("Vui lòng nhập mật khẩu")
                else:
                    st.error("Tài khoản hoặc mật khẩu không đúng")
                self.data_user.closeSQL() 

    def getStatusLogin(self):
        return st.session_state.check_login

