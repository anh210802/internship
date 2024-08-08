import streamlit as st
from streamlit_option_menu import option_menu
from FontEnd.home import Home
from FontEnd.account import Account
from FontEnd.monitor import Monitor
from FontEnd.history import History



class Sidebar:
    def __init__(self, _home=Home(), _account=Account(), _monitor=Monitor(), _history=History()):
        self.home = _home
        self.account = _account
        self.monitor = _monitor
        self.history = _history
    
    def run(self):
        st.set_page_config(page_title="Hệ thống giám sát môi trường",
                           page_icon=":globe_with_meridians:",
                           layout="wide")
        with st.sidebar:
            selected_page = option_menu(
                menu_title="Menu",
                options=["Home", "Tài khoản", "Quan sát", "Lịch sử"],
                icons=["house", "person-circle", "gear", "book"],
                menu_icon="cast",
                default_index=0
            )

        if selected_page == "Home":
            self.home.app()
        elif selected_page == "Tài khoản":
            self.account.app()
        elif selected_page == "Quan sát":
            self.monitor.app(self.account.getStatusLogin())
            # self.monitor.app(True)
        elif selected_page == "Lịch sử":
            self.history.app(self.account.getStatusLogin())
            # self.history.app(True)


