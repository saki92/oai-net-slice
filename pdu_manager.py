import socket

def input_data():
    send_cmd = int(input("Enter the option here: "))
    if send_cmd == 1:
        pdu_id = int(input("Enter new session id: "))
        if pdu_id in pdu_session_active:
            print("Entered session id already active")
            data = input_data()
        else:
            data1 = send_cmd.to_bytes(1, 'little')
            data2 = pdu_id.to_bytes(1, 'little')
            data = data1 + data2
    elif send_cmd == 2:
        pdu_id = int(input("Enter PDU session id to delete: "))
        if pdu_id in pdu_session_active:
            data1 = send_cmd.to_bytes(1, 'little')
            data2 = pdu_id.to_bytes(1, 'little')
            data = data1 + data2
        else:
            print("Entered PDU session not active")
            data = input_data()
    else:
        print("Invalid option")
        data = input_data()
    return data

def main():
# Define the server address and port
    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 34000

# Define the data to send
    data = b'Hello, server!'

# Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    try:
        while True:
# Send the data
            client_socket.sendall(data)

# Receive data
            rec_data = client_socket.recv(1024)
#print(rec_data.hex())
            rec_data_l = list(rec_data)
            num_elm = rec_data_l[0] | (rec_data_l[1]<<15)
            print()
            print("Number of SDAP entities: ", num_elm)

            l = range(2, 2+num_elm*2, 2)
            num = 0
            for i in l:
                num += 1
                print(num, ":")
                entity_num = rec_data[i]
                print("  SDAP entity index: ", entity_num)
                pdusession_id = rec_data[i+1]
                pdu_session_active.append(pdusession_id)
                print("  PDU session id :", pdusession_id)

            print()
            print("Enter any of the following commands to send")
            print("  Request new PDU session: 1")
            print("  Request deletion of PDU session: 2")
            data = input_data()
    finally:
# Close the socket
        client_socket.close()

if __name__ == '__main__':
    pdu_session_active = []
    main()
