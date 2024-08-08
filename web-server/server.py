import socket
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from BackEnd.connectSQLite import SQLite
import datetime

class Server:
    def __init__(self, _host, _port):
        self.host = _host
        self.port = _port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.is_running = True
        self.lock = Lock()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started at {self.host}:{self.port}")
        print("Waiting for connections...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            while self.is_running:
                try:
                    self.server_socket.settimeout(1.0)
                    client_socket, addr = self.server_socket.accept()
                    print(f"Got a connection from {addr}")
                    future = executor.submit(self.readDataGateWay, client_socket, addr)
                    self.clients.append((future, client_socket))
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error accepting connection: {e}")

            for future, client_socket in self.clients:
                client_socket.close()
                try:
                    future.result()
                except Exception as e:
                    print(f"Error handling client: {e}")

    def readDataGateWay(self, client_socket, addr):
        conn = None
        try:
            conn = SQLite("BackEnd/data_sql.sqlite")
            conn.connectSQL()
            cursor = conn.cursor
            while self.is_running:
                try:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    # print(f"Received from {addr}: {data}")
                    split_data = data.split('-')
                    if len(split_data) >= 7:
                        temp = float(split_data[1])
                        humi = float(split_data[2])
                        pm1 = float(split_data[3])
                        pm25 = float(split_data[4])
                        pm10 = float(split_data[5])
                        CO_value = float(split_data[6])
                        max_value = max(pm1, pm25, pm10, CO_value)
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        level = self.calculate_level(max_value)

                        print(f"Received from {addr}: {temp}, {humi}, {pm1}, {pm25}, {pm10}, {CO_value}, {max_value}, {level}, {now}")
                        with self.lock:
                            cursor.execute(
                                "INSERT INTO sensor_data (temperature, humidity, pm1, pm25, pm10, co_value, max_value, level, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (temp, humi, pm1, pm25, pm10, CO_value, max_value, level, now)
                            )
                            conn.conn.commit()
                        print("Data inserted into database")
                    else:
                        print(f"Incomplete data received from {addr}: {split_data}")
                except Exception as e:
                    print(f"Error handling data from {addr}: {e}")
                    break

        except Exception as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.closeSQL()
            client_socket.close()
            print(f"Connection from {addr} closed")

    def calculate_level(self, max_value):
        if max_value <= 50:
            return 1
        elif max_value <= 150:
            return 2
        else:
            return 3

    def stop(self):
        self.is_running = False
        self.server_socket.close()
        for future, client_socket in self.clients:
            try:
                client_socket.close()
                future.result()
            except Exception as e:
                print(f"Error closing client connection: {e}")
        print("Server stopped")


if __name__ == "__main__":
    server = Server("177.30.34.202", 2108)
    server.start()