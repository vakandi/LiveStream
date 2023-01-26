import requests

def stop_server():
    try:
        requests.get("http://localhost:8055/shutdown")
        print("Server stopped successfully.")
    except:
        print("Failed to stop server. Make sure the server is running and the correct host and port are being used.")

if __name__ == '__main__':
    stop_server()

