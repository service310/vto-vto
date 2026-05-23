rom fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>全雙工語音機器人</title>
</head>
<body>
    <h1>全雙工語音機器人測試</h1>
    <div id="chat" style="border:1px solid #ccc;height:400px;overflow-y:auto;padding:10px;"></div>
    <input id="msg" placeholder="輸入訊息..." style="width:80%;padding:10px;">
    <button onclick="send()">發送</button>

    <script>
        const ws = new WebSocket(`wss://${window.location.host}/ws`);
        const chat = document.getElementById('chat');

        ws.onmessage = function(e) {
            const p = document.createElement('p');
            p.innerHTML = `<b>機器人：</b> ${e.data}`;
            chat.appendChild(p);
            chat.scrollTop = chat.scrollHeight;
        };

        function send() {
            const input = document.getElementById('msg');
            if (!input.value.trim()) return;
            const p = document.createElement('p');
            p.innerHTML = `<b>你：</b> ${input.value}`;
            chat.appendChild(p);
            ws.send(input.value);
            input.value = '';
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"收到你的訊息：「{data}」\n我正在思考怎麼回覆你～（全雙工測試成功！）")
    except WebSocketDisconnect:
        pass
