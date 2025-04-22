import os
from flask import Flask, request
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
import openai

load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body", "").strip()
    response = MessagingResponse()
    msg = response.message()

    classification, reply = generate_reply(incoming_msg)
    msg.body(reply)
    return str(response)

def generate_reply(message):
    system_prompt = """أنت مساعد ذكي وظيفتك هي الرد على العملاء المهتمين بمنتج زيت شعر طبيعي يُدعى Misal. 
مهمتك تقنعهم بالشراء، تجاوب على أسئلتهم، وتطلب بياناتهم لما يكونوا جاهزين للطلب. 
معلومات المنتج:
- الاسم: زيت شعر Misal
- الحجم: 100 مل
- السعر: 120 دينار ليبي مع شحن مجاني خلال 3 أيام
- الاستخدام: 3 مرات بالأسبوع
- مناسب للرجال والنساء
- فوائد: يمنع التساقط، يقوي البصيلات، يطول الشعر، ينعمو، يعالج الفراغات
- الرائحة: مزيج النعناع وإكليل الجبل (قوية للأطفال لكنها تختفي بعد شوي)
- طريقة الاستخدام: مثل أي زيت عادي، يدلك به فروة الرأس ويترك على الأقل ساعة
- الطلب يحتاج: الاسم، العنوان، رقم الهاتف
- مناسب لجميع الأعمار، ويعتبر حل نهائي للتساقط عند الاستخدام الصحيح"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )
        reply = completion.choices[0].message["content"].strip()
    except Exception as e:
        reply = "صار خلل بسيط، جرب تبعتلنا من جديد بالله."

    return "general", reply

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
