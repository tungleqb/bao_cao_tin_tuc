import asyncio
import websockets
import requests

# Đăng nhập để lấy token
LOGIN_URL = "http://localhost:8000/auth/login"
login_data = {
    "username": "tester2",
    "password": "123457",
    "role": "llm_host"
}
resp = requests.post(LOGIN_URL, json=login_data)
if resp.status_code != 200:
    print("❌ Login thất bại:", resp.status_code, resp.text)
    exit(1)
token = resp.json()["access_token"]

# Gửi token lên WebSocket
async def connect_ws():
    ws_url = f"ws://localhost:8000/ws/host?token={token}"
    async with websockets.connect(ws_url) as websocket:
        print("✅ Đã kết nối WebSocket thành công!")
        greeting = await websocket.recv()
        print("📨 Server gửi:", greeting)

asyncio.run(connect_ws())
