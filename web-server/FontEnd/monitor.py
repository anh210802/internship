import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from BackEnd.connectSQLite import SQLite
import time

class Monitor:
    def __init__(self) -> None:
        self.db = SQLite("BackEnd/data_sql.sqlite")
        self.check_login = False
        self.pre_temp = 0
        self.pre_humi = 0
        self.pre_co = 0
        self.pre_pm1 = 0
        self.pre_pm25 = 0
        self.pre_pm10 = 0

    def app(self, log):
        self.check_login = log
        self.db.connectSQL()
        st.subheader('Hệ thống giám sát môi trường', divider='rainbow')
        st.subheader('_Giám sát cảm biến_')

        if self.check_login:
            self.initialize_session_state()
            self.updateData()

            header = st.container()
            col1, col2, col3 = header.columns(3)

            with col1:
                st.metric("Nhiệt độ", f"{st.session_state.temp} °C", f"{st.session_state.pre_temp}°C")
            with col2:
                st.metric("Độ ẩm", f"{st.session_state.humi} %", f"{st.session_state.pre_humi}%")
            with col3:
                st.metric("Khí CO", f"{st.session_state.co} ppm", f"{st.session_state.pre_co}ppm")

            header = st.container()
            col1, col2, col3 = header.columns(3)

            with col1:
                st.metric("PM 1", f"{st.session_state.pm1} µg/m³", f"{st.session_state.pre_pm1}µg/m³")
            with col2:
                st.metric("PM 2.5", f"{st.session_state.pm25} µg/m³", f"{st.session_state.pre_pm25}µg/m³")
            with col3:
                st.metric("PM 10", f"{st.session_state.pm10} µg/m³", f"{st.session_state.pre_pm10}µg/m³")

            style_metric_cards(
                "#FFFFFF",
                2,
                "#CCC",
                5,
                "#9AD8E1",
                True,
            )

            # Set a time interval for auto-refresh
            time.sleep(1)
            self.db.closeSQL()
            st.rerun()

        else:
            st.write("Bạn chưa đăng nhập. Hãy đăng nhập để sử dụng hệ thống.")

    def initialize_session_state(self):
        if 'last_update_time' not in st.session_state:
            st.session_state.last_update_time = 0
            st.session_state.temp = 0
            st.session_state.humi = 0
            st.session_state.co = 0
            st.session_state.pm1 = 0
            st.session_state.pm25 = 0
            st.session_state.pm10 = 0

    def updateData(self):
        current_time = time.time()
        if current_time - st.session_state.last_update_time >= 10:
            data = self.db.showRealTimeData()
            if data:
                self.pre_temp = st.session_state.temp
                self.pre_humi = st.session_state.humi
                self.pre_co = st.session_state.co
                self.pre_pm1 = st.session_state.pm1
                self.pre_pm25 = st.session_state.pm25
                self.pre_pm10 = st.session_state.pm10

                st.session_state.temp = data[1]
                st.session_state.humi = data[2]
                st.session_state.pm1 = data[3]
                st.session_state.pm25 = data[4]
                st.session_state.pm10 = data[5]
                st.session_state.co = data[6]

                st.session_state.pre_temp = st.session_state.temp - self.pre_temp
                st.session_state.pre_humi = st.session_state.humi - self.pre_humi
                st.session_state.pre_co = st.session_state.co - self.pre_co
                st.session_state.pre_pm1 = st.session_state.pm1 - self.pre_pm1
                st.session_state.pre_pm25 = st.session_state.pm25 - self.pre_pm25
                st.session_state.pre_pm10 = st.session_state.pm10 - self.pre_pm10

            st.session_state.last_update_time = current_time
