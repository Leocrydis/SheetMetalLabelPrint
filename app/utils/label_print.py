import socket

def print_label(zpl_command, label_type):
    printer_ip = "192.168.1.202"  # Default IP for SS
    if label_type == "2B" or label_type == "CSV" or label_type == "GL":
        printer_ip = "192.168.1.238"
    printer_port = 9100

    try:
        # Try to send the ZPL command to the printer over a network socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as zebra_socket:
            zebra_socket.connect((printer_ip, printer_port))
            zebra_socket.sendall(zpl_command.encode('utf-8'))
            print(f"Label sent to Zebra printer at {printer_ip}:{printer_port}")
    except Exception as e:
        print(f"Error sending label to Zebra printer: {e}")
        print("Attempting to find the printer by name...")