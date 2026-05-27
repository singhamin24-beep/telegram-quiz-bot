import logging
import asyncio
import os
from telegram import Update, Poll
from telegram.ext import Application, CommandHandler, ContextTypes, PollAnswerHandler
from questions import QUESTIONS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable नहीं मिला!")

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎓 GK Quiz Bot में आपका स्वागत है!\n\n"
        "📚 विषय: इतिहास, राजव्यवस्था, रसायन विज्ञान, GK\n"
        "❓ कुल प्रश्न: 25\n\n"
        "▶️ शुरू करने के लिए /quiz टाइप करें\n"
        "📊 स्कोर देखने के लिए /score टाइप करें"
    )

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {
        "current": 0,
        "score": 0,
        "wrong": [],
        "chat_id": update.effective_chat.id
    }
    await send_question(update.effective_chat.id, user_id, context)

async def send_question(chat_id, user_id, context):
    data = user_data.get(user_id)
    if not data:
        return
    idx = data["current"]
    if idx >= len(QUESTIONS):
        await show_result(chat_id, user_id, context)
        return
    q = QUESTIONS[idx]
    topic_emoji = {
        "प्राचीन इतिहास": "🏰",
        "मध्यकालीन इतिहास": "⚔️",
        "आधुनिक इतिहास": "🚩",
        "भारतीय राजव्यवस्था": "⚖️",
        "रसायन विज्ञान": "🧪",
        "सांख्यिकी GK": "📊",
        "सामान्य ज्ञान": "💡"
    }
    emoji = topic_emoji.get(q["topic"], "📚")
    await context.bot.send_poll(
        chat_id=chat_id,
        question=f"{emoji} Q{idx+1}/25 [{q['topic']}]\n\n{q['q']}",
        options=q["opts"],
        type=Poll.QUIZ,
        correct_option_id=q["ans"],
        explanation=f"✅ {q['exp']}\n\n💡 ट्रिक: {q['trick']}",
        is_anonymous=False,
        open_period=30
    )

async def handle_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    user_id = answer.user.id
    data = user_data.get(user_id)
    if not data:
        return
    q = QUESTIONS[data["current"]]
    selected = answer.option_ids[0] if answer.option_ids else -1
    if selected == q["ans"]:
        data["score"] += 1
    else:
        data["wrong"].append(q)
    data["current"] += 1
    await asyncio.sleep(2)
    await send_question(data["chat_id"], user_id, context)

async def show_result(chat_id, user_id, context):
    data = user_data.get(user_id)
    if not data:
        return
    score = data["score"]
    total = len(QUESTIONS)
    pct = round(score / total * 100)
    if pct >= 80:
        grade = "🏆 उत्कृष्ट!"
    elif pct >= 60:
        grade = "👍 बहुत अच्छे!"
    elif pct >= 40:
        grade = "📚 ठीक है!"
    else:
        grade = "💪 और मेहनत करें!"
    result_text = (
        f"🎉 क्विज़ पूरा हुआ!\n\n"
        f"✅ सही उत्तर: {score}/{total}\n"
        f"📊 प्रतिशत: {pct}%\n"
        f"🎯 {grade}\n\n"
    )
    if data["wrong"]:
        result_text += "❌ गलत उत्तरों की ट्रिक्स:\n\n"
        for i, q in enumerate(data["wrong"], 1):
            result_text += (
                f"Q{i}. {q['q']}\n"
                f"✅ सही: {q['opts'][q['ans']]}\n"
                f"💡 ट्रिक: {q['trick']}\n\n"
            )
    else:
        result_text += "🌟 शाबाश! सभी उत्तर सही थे!"
    result_text += "\n▶️ फिर खेलने के लिए /quiz टाइप करें"
    await context.bot.send_message(
        chat_id=chat_id,
        text=result_text
    )

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = user_data.get(user_id)
    if not data:
        await update.message.reply_text("पहले /quiz से quiz शुरू करें!")
        return
    await update.message.reply_text(
        f"📊 आपका अभी तक का स्कोर:\n"
        f"✅ सही: {data['score']}/{data['current']}"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("score", score))
    app.add_handler(PollAnswerHandler(handle_poll_answer))
    print("✅ Bot चालू हो गया!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
