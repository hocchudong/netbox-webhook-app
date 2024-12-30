from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = '2004478698:AAEsHPaCw_xxxxxxxxxxxxxxxxxxxx'  # Thay thế bằng token của bot Telegram của bạn
TELEGRAM_CHAT_ID = 'xxxxxxxxxxx'  # Thay thế bằng chat ID của bạn hoặc nhóm

def send_telegram_message(message):
    """
    Gửi tin nhắn tới Telegram sử dụng bot API.
    """
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(url, json=payload)
    return response

def handle_webhook(data):
    """
    Hàm để xử lý dữ liệu webhook nhận được từ NetBox và in ra màn hình.
    """
    print("Webhook received!")
    print(data)

    # Hiển thị chi tiết cập nhật nếu có
    message = "Webhook received!\n"
    if 'event' in data:
        message += f"Event: {data['event']}\n"
    if 'timestamp' in data:
        message += f"Timestamp: {data['timestamp']}\n"

    rack_data = str(data.get('data', {}).get('rack'))
    print(rack_data)
    print("#################################3333")
    if rack_data == "None":
        rack_name_hien_tai = "KHONG CO GIA TRI"
        print(rack_name_hien_tai)
        rack_name_truoc = data['snapshots']['prechange']['rack']
        message += f"Rack hien tai: {rack_name_hien_tai} \nRack truoc: {rack_name_truoc}\n"
        send_telegram_message(message)  # Gửi thông báo tới Telegram

    if rack_data != "None":
        rack_name_hien_tai = data['data']['rack']['name']
        print(rack_name_hien_tai)
        rack_name_truoc = data['snapshots']['prechange']['rack']
        message += f"Rack hien tai: {rack_name_hien_tai} \nRack truoc: {rack_name_truoc}\n"
        send_telegram_message(message)  # Gửi thông báo tới Telegram


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        handle_webhook(data)  # Gọi hàm handle_webhook và truyền dữ liệu nhận được

        # In thông báo ra màn hình trước khi trả về phản hồi
        response_message = {'message': 'Webhook received!'}
        print(f"Returning response: {response_message}, Status code: 200")

        return jsonify(response_message), 200  # Trả về phản hồi HTTP 200 OK
    else:
        return jsonify({'message': 'Method not allowed'}), 405  # Trả về phản hồi HTTP 405 Method Not Allowed

if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)
