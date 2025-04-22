from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils.openai_handler import analyze_message
from utils.excel_logger import log_order
from utils.voice_transcriber import transcribe_audio
import os

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").strip()
    media_content_type = request.values.get("MediaContentType0", "")
    media_url = request.values.get("MediaUrl0", "")

    response = MessagingResponse()
    msg = response.message()

    if "audio" in media_content_type:
        transcript = transcribe_audio(media_url)
        incoming_msg = transcript or "ما قدرت أسمع التسجيل، ممكن تعيد بصيغة أوضح؟"

    reply, order_data = analyze_message(incoming_msg)

    if order_data:
        log_order(order_data)

    msg.body(reply)
    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)