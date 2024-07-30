from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging

# إعداد التسجيل لعرض الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# الدالة التي تقوم بحساب المبلغ الذي ستستلمه بعد خصم الرسوم
def calculate_received_amount(amount_to_deduct: float) -> float:
    fee_percentage = 0.57 / 100
    received_amount = amount_to_deduct / (1 + fee_percentage)
    return round(received_amount, 2)

# دالة لتعامل مع الأمر /start
async def start(update: Update, context) -> None:
    logger.info("Received /start command")
    await update.message.reply_text('مرحبا! أرسل لي المبلغ الذي ترغب في خصمه من المحفظة وسأحسب لك المبلغ الذي ستستلمه.')

# دالة لتعامل مع الرسائل النصية
async def handle_message(update: Update, context) -> None:
    logger.info("Received message: %s", update.message.text)
    try:
        # قراءة المبلغ من الرسالة
        amount_to_deduct = float(update.message.text)
        
        # حساب المبلغ الذي ستستلمه
        received_amount = calculate_received_amount(amount_to_deduct)
        
        # إرسال النتيجة إلى المستخدم
        await update.message.reply_text(f"{received_amount:.2f}")
    except ValueError:
        logger.error("ValueError: Invalid amount entered")
        await update.message.reply_text("يرجى إدخال مبلغ صحيح.")

def main() -> None:
    # التوكن الخاص بالبوت
    TOKEN = '6327653741:AAE4g-cqpc4j7-ApsMsUP8WlCE7RzUwiixA'
    
    # إعداد البوت
    application = Application.builder().token(TOKEN).build()
    
    # إضافة معالجين للأوامر والرسائل
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # بدء تشغيل البوت
    logger.info("Starting bot")
    application.run_polling()

if __name__ == '__main__':
    main()
