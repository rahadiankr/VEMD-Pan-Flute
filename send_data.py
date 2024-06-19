import time
import socket
import streamlit as st
import pickle # If want to share array data

UDP_IP = "192.168.1.255"
UDP_PORT = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

class sending_data:
    # def close_socket():
    #     sock.close()
    #     return True
        
    def send_data_to_plc(data_to_send):
        def stopper(x):
            with_stopper = []
            for index, item in enumerate(x):
                with_stopper.append(item)
                if index + 1 != len(x):
                    with_stopper.append((x[index][1], x[index + 1][0], x[index][2], 1))
                else:
                    with_stopper.append((x[index][1], x[index][1], x[index][2], 1))
            return with_stopper
            # stopper = (x[len(x) - 1][1], x[len(x) - 1][1], x[len(x) - 1][2], 1)
            # x.append(stopper)
            return x

        x = stopper(data_to_send)

        def send_data(data1, data2, data3):
            data3 = round(data3*1000)
            buffer_data1 = data1.to_bytes(2, byteorder='little')
            buffer_data2 = data2.to_bytes(2, byteorder='little')
            buffer_data3 = data3.to_bytes(2, byteorder='little')

            buffer_to_send = buffer_data1 + buffer_data2 + buffer_data3
            # print(' '.join(f'{byte:02x}' for byte in buffer_to_send), end=' ')
            print(f"sending index:{data1}, flow:{data2}, and duration:{data3} to {UDP_IP}:{UDP_PORT}")

            sock.sendto(buffer_to_send, (UDP_IP, UDP_PORT))

            # stopper1 = 17
            # stopper2 = 1
            # stopper3 = 0
            # stopper_data1 = stopper1.to_bytes(2, byteorder='little')
            # stopper_data2 = stopper2.to_bytes(2, byteorder='little')
            # stopper_data3 = stopper3.to_bytes(2, byteorder='little')
            # stopper_to_send = stopper_data1 + stopper_data2 + stopper_data3
            # sock.sendto(stopper_to_send, (UDP_IP, UDP_PORT))

        # Loop through the list of tuples
        count = len(x)
        i = 0
        first = 0
        last_note = None
        while i < count and st.session_state.stop is not True:
            if st.session_state.stop:
                break
            start_time = x[i][0]
            end_time = x[i][1]
            index_vemd = x[i][2]  # data that goes into the index vemd to select which vemd is active (-1 - 15) or (tone 712345671234567)
            flow_range = x[i][3]  # flow opening size data (0-100)

            # Calculate the duration and interval to sleep
            interval = start_time - first
            duration = end_time - start_time

            if last_note != None:
                if (index_vemd-last_note >= 7):
                    last_note = index_vemd
                    continue;

            if interval < 0 or duration < 0:
                interval = 0.0
                duration = 0.0
                time.sleep(interval)
                # print("============================================================")
                # print(f"First:{first}\nStart:{start_time}\nEnd:{end_time}\nInterval:{interval}\nDuration:{duration}")
            else:
                time.sleep(interval)
                print("============================================================")
                print(f"Note:{index_vemd} / {start_time}")
                # print(f"Note:{index_vemd} / {start_time}\nFirst:{first}\nStart:{start_time}\nEnd:{end_time}\nInterval:{interval}\nDuration:{duration}")

            # Send the data
            send_data(index_vemd, flow_range, duration)
            first = start_time
            last_note = index_vemd
            print(f"SELESAI {duration}")
            i+=1


        # After sending all data
        print("All data sent.")