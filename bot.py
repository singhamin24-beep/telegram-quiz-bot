import telebot
import random
import time
from telebot.types import Poll

BOT_TOKEN = "8930549590:AAEsQ-IxHuJFrU9OkYS3dvRklW-Gq4lD5Vw"
bot = telebot.TeleBot(BOT_TOKEN)

ALL_QUESTIONS = [
    {"topic":"प्राचीन इतिहास","q":"हड़प्पा सभ्यता की खोज किस वर्ष हुई?","opts":["1920","1921","1922","1923"],"ans":1,"trick":"1921 में हड़प्पा मिला — '21 सालूम हड़प्पा'"},
    {"topic":"प्राचीन इतिहास","q":"मौर्य साम्राज्य की स्थापना किसने की?","opts":["अशोक","बिंदुसार","चंद्रगुप्त मौर्य","समुद्रगुप्त"],"ans":2,"trick":"चंद्र = पहला मौर्य"},
    {"topic":"प्राचीन इतिहास","q":"अर्थशास्त्र की रचना किसने की?","opts":["मनु","चाणक्य","वाल्मीकि","कालिदास"],"ans":1,"trick":"Chanakya = Chancellor = Economy"},
    {"topic":"प्राचीन इतिहास","q":"कलिंग युद्ध कब हुआ?","opts":["261 ई.पू.","250 ई.पू.","272 ई.पू.","232 ई.पू."],"ans":0,"trick":"261 = 2+6+1 = 9 = शांति का अंक"},
    {"topic":"प्राचीन इतिहास","q":"बौद्ध धर्म के संस्थापक कौन थे?","opts":["महावीर","गौतम बुद्ध","आदिनाथ","नागार्जुन"],"ans":1,"trick":"बुद्ध = बुद्धि = ज्ञान"},
    {"topic":"प्राचीन इतिहास","q":"गुप्त वंश का स्वर्णकाल किसके काल में था?","opts":["चंद्रगुप्त I","समुद्रगुप्त","चंद्रगुप्त II","कुमारगुप्त"],"ans":2,"trick":"II = Double Gold = स्वर्णकाल"},
    {"topic":"प्राचीन इतिहास","q":"तक्षशिला किस क्षेत्र में था?","opts":["मगध","गांधार","पाटलिपुत्र","मथुरा"],"ans":1,"trick":"TaKSHila = गंधार"},
    {"topic":"प्राचीन इतिहास","q":"महाभारत की रचना किसने की?","opts":["वाल्मीकि","तुलसीदास","वेदव्यास","कालिदास"],"ans":2,"trick":"Vyas = Vyapak = बड़ा ग्रंथ"},
    {"topic":"मध्यकालीन इतिहास","q":"दिल्ली सल्तनत की स्थापना किसने की?","opts":["इल्तुतमिश","कुतुबुद्दीन ऐबक","बलबन","रजिया"],"ans":1,"trick":"कुतुब = कुतुब मीनार = पहला सुल्तान"},
    {"topic":"मध्यकालीन इतिहास","q":"पानीपत की पहली लड़ाई कब हुई?","opts":["1526","1556","1761","1520"],"ans":0,"trick":"1526 = बाबर का नंबर"},
    {"topic":"मध्यकालीन इतिहास","q":"ताजमहल किसने बनवाया?","opts":["अकबर","जहाँगीर","शाहजहाँ","औरंगजेब"],"ans":2,"trick":"Taj = शाहजहाँ का ताज"},
    {"topic":"मध्यकालीन इतिहास","q":"हल्दीघाटी युद्ध किनके बीच हुआ?","opts":["अकबर-प्रताप","बाबर-राणा सांगा","हुमायूँ-शेरशाह","औरंगजेब-दारा"],"ans":0,"trick":"हल्दी = Yellow = Akbar vs Pratap"},
    {"topic":"मध्यकालीन इतिहास","q":"शेरशाह सूरी का असली नाम क्या था?","opts":["फरीद खान","हसन खान","यूसुफ खान","अली खान"],"ans":0,"trick":"F=Farid = First Afghan King"},
    {"topic":"मध्यकालीन इतिहास","q":"मुगल साम्राज्य का अंतिम सम्राट कौन था?","opts":["शाहजहाँ","बहादुर शाह I","बहादुर शाह जफर","औरंगजेब"],"ans":2,"trick":"जफर = आखिरी = Zafar ends with r = End"},
    {"topic":"मध्यकालीन इतिहास","q":"अकबर ने दीन-ए-इलाही कब शुरू किया?","opts":["1578","1580","1582","1585"],"ans":2,"trick":"1582 = दीन-ए-दो"},
    {"topic":"मध्यकालीन इतिहास","q":"विजयनगर साम्राज्य की स्थापना किसने की?","opts":["हरिहर-बुक्का","देवराय I","कृष्णदेव राय","विरूपाक्ष"],"ans":0,"trick":"H+B = HB Pencil जैसे जोड़ी"},
    {"topic":"आधुनिक इतिहास","q":"1857 की क्रांति को क्या कहते हैं?","opts":["सिपाही विद्रोह","नील विद्रोह","संथाल विद्रोह","चंपारण"],"ans":0,"trick":"1857 = सिपाही"},
    {"topic":"आधुनिक इतिहास","q":"भारत का पहला गवर्नर जनरल कौन था?","opts":["डलहौजी","वॉरेन हेस्टिंग्स","बेंटिक","कर्जन"],"ans":1,"trick":"WARREN = W = पहला अक्षर = पहले GG"},
    {"topic":"आधुनिक इतिहास","q":"कांग्रेस की स्थापना कब हुई?","opts":["1882","1883","1884","1885"],"ans":3,"trick":"INC = 1885"},
    {"topic":"आधुनिक इतिहास","q":"जलियांवाला बाग हत्याकांड कब हुआ?","opts":["1917","1918","1919","1920"],"ans":2,"trick":"1919 = 19+19 = दोहरी त्रासदी"},
    {"topic":"आधुनिक इतिहास","q":"'करो या मरो' नारा किसने दिया?","opts":["नेहरू","बोस","गांधी","तिलक"],"ans":2,"trick":"Gandhi = करो या मरो"},
    {"topic":"आधुनिक इतिहास","q":"भारत को स्वतंत्रता कब मिली?","opts":["14 अगस्त 1947","15 अगस्त 1947","26 जनवरी 1947","15 अगस्त 1948"],"ans":1,"trick":"15 August = 🇮🇳"},
    {"topic":"आधुनिक इतिहास","q":"संविधान सभा के अध्यक्ष कौन थे?","opts":["राजेंद्र प्रसाद","अंबेडकर","नेहरू","पटेल"],"ans":0,"trick":"R.P. = President of Assembly"},
    {"topic":"भारतीय राजव्यवस्था","q":"संविधान में मूल अनुच्छेद कितने थे?","opts":["395","444","448","470"],"ans":0,"trick":"395 = 3-9-5 याद करो"},
    {"topic":"भारतीय राजव्यवस्था","q":"राष्ट्रपति का कार्यकाल कितना होता है?","opts":["4 वर्ष","5 वर्ष","6 वर्ष","जीवनभर"],"ans":1,"trick":"5 = FIVE = P-R-E-S-I = 5 letters"},
    {"topic":"भारतीय राजव्यवस्था","q":"लोकसभा का कार्यकाल कितना होता है?","opts":["4 वर्ष","5 वर्ष","6 वर्ष","3 वर्ष"],"ans":1,"trick":"लोकसभा = 5 = PANCH"},
    {"topic":"भारतीय राजव्यवस्था","q":"राज्यसभा सदस्यों का कार्यकाल कितना होता है?","opts":["4 वर्ष","5 वर्ष","6 वर्ष","जीवनभर"],"ans":2,"trick":"राज्यसभा SENIOR = 6 साल"},
    {"topic":"भारतीय राजव्यवस्था","q":"मौलिक अधिकार किस भाग में हैं?","opts":["भाग II","भाग III","भाग IV","भाग V"],"ans":1,"trick":"III = 3 = मौलिक अधिकार"},
    {"topic":"भारतीय राजव्यवस्था","q":"42वें संशोधन में क्या जोड़ा गया?","opts":["पंथनिरपेक्ष","समाजवादी","दोनों","कोई नहीं"],"ans":2,"trick":"42 = दोनों एक साथ"},
    {"topic":"भारतीय राजव्यवस्था","q":"सर्वोच्च न्यायालय कहाँ है?","opts":["मुंबई","चेन्नई","नई दिल्ली","कोलकाता"],"ans":2,"trick":"Supreme = Capital = Delhi"},
    {"topic":"रसायन विज्ञान","q":"पानी का सूत्र क्या है?","opts":["HO","H2O","H3O","H2O2"],"ans":1,"trick":"H-2-O = हम दो हमारा एक!"},
    {"topic":"रसायन विज्ञान","q":"सोडियम का प्रतीक क्या है?","opts":["So","Na","Sd","S"],"ans":1,"trick":"Na = Natrium = नमक"},
    {"topic":"रसायन विज्ञान","q":"हवा में नाइट्रोजन कितना है?","opts":["21%","40%","78%","90%"],"ans":2,"trick":"N=78 = सात-आठ"},
    {"topic":"रसायन विज्ञान","q":"नमक का रासायनिक नाम?","opts":["सोडियम कार्बोनेट","सोडियम क्लोराइड","सोडियम हाइड्रोक्साइड","सोडियम सल्फेट"],"ans":1,"trick":"NaCl = नमक"},
    {"topic":"रसायन विज्ञान","q":"ऑक्सीजन की परमाणु संख्या?","opts":["6","7","8","9"],"ans":2,"trick":"O = 8 = आठ"},
    {"topic":"रसायन विज्ञान","q":"बेकिंग सोडा का नाम?","opts":["सोडियम कार्बोनेट","सोडियम बाइकार्बोनेट","सोडियम हाइड्रोक्साइड","कैल्शियम कार्बोनेट"],"ans":1,"trick":"BAKING = BI = Bi-carbonate"},
    {"topic":"रसायन विज्ञान","q":"सबसे हल्का तत्व कौन सा है?","opts":["हीलियम","नाइट्रोजन","हाइड्रोजन","लिथियम"],"ans":2,"trick":"H = 1 = Ek = पहला = सबसे हल्का"},
    {"topic":"रसायन विज्ञान","q":"पीतल किससे बनता है?","opts":["लोहा-तांबा","जिंक-तांबा","एल्युमिनियम-तांबा","निकल-तांबा"],"ans":1,"trick":"Brass = Zinc+Copper = Z+C"},
    {"topic":"सांख्यिकी GK","q":"2011 में भारत की जनसंख्या?","opts":["110 करोड़","121 करोड़","130 करोड़","125 करोड़"],"ans":1,"trick":"2011 = 121 = 11²"},
    {"topic":"सांख्यिकी GK","q":"सबसे बड़ा राज्य (क्षेत्रफल)?","opts":["मध्यप्रदेश","महाराष्ट्र","राजस्थान","उत्तरप्रदेश"],"ans":2,"trick":"RAJ = बड़े राजा का बड़ा राज्य"},
    {"topic":"सांख्यिकी GK","q":"सर्वाधिक जनसंख्या वाला राज्य?","opts":["महाराष्ट्र","बिहार","उत्तरप्रदेश","पश्चिम बंगाल"],"ans":2,"trick":"UP = सबसे ऊपर = No.1"},
    {"topic":"सांख्यिकी GK","q":"भारत में कुल राज्य?","opts":["28","29","30","31"],"ans":0,"trick":"28 = 4×7"},
    {"topic":"सांख्यिकी GK","q":"सबसे छोटा राज्य (क्षेत्रफल)?","opts":["सिक्किम","त्रिपुरा","गोवा","मणिपुर"],"ans":2,"trick":"GOA = Go-Small!"},
    {"topic":"सांख्यिकी GK","q":"2011 में साक्षरता दर?","opts":["64.8%","74.04%","80.2%","70%"],"ans":1,"trick":"74 = साक्षर"},
    {"topic":"सांख्यिकी GK","q":"सर्वाधिक लिंगानुपात वाला राज्य?","opts":["केरल","तमिलनाडु","हिमाचलप्रदेश","गोवा"],"ans":0,"trick":"Kerala = K = Ladies First"},
    {"topic":"सामान्य ज्ञान","q":"'इंकलाब जिंदाबाद' किसने दिया?","opts":["भगत सिंह","सुभाष बोस","लाला लाजपत राय","आजाद"],"ans":0,"trick":"Inquilab = I = I am Bhagat Singh!"},
    {"topic":"सामान्य ज्ञान","q":"सबसे बड़ा महासागर?","opts":["हिंद","अटलांटिक","प्रशांत","आर्कटिक"],"ans":2,"trick":"PACIFIC = P = Pehla = No.1"},
    {"topic":"सामान्य ज्ञान","q":"भारत का राष्ट्रीय खेल?","opts":["क्रिकेट","हॉकी","कबड्डी","फुटबॉल"],"ans":1,"trick":"Hockey = H = हिंदुस्तान"},
    {"topic":"सामान्य ज्ञान","q":"'सत्यमेव जयते' कहाँ से लिया गया?","opts":["ऋग्वेद","मुण्डक उपनिषद","तैत्तिरीय उपनिषद","छान्दोग्य"],"ans":1,"trick":"MUNdak = सत्य बोलो"},
    {"topic":"सामान्य ज्ञान","q":"भारत का सबसे लंबा नदी कौन सी है?","opts":["यमुना","गंगा","गोदावरी","नर्मदा"],"ans":1,"trick":"गंगा = G = Greatest = सबसे लंबी"},
]

user_sessions = {}

def get_random_questions():
    return random.sample(ALL_QUESTIONS, min(25, len(ALL_QUESTIONS)))

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "🎓 *GK Quiz Bot में आपका स्वागत है!*\n\n"
        "📚 विषय: इतिहास, राजव्यवस्था, रसायन, GK\n"
        "❓ हर बार अलग 25 प्रश्न\n\n"
        "▶️ /quiz — क्विज़ शुरू करें\n"
        "📊 /score — स्कोर देखें\n"
        "ℹ️ /help — सहायता",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message,
        "📖 *सहायता*\n\n"
        "/quiz — नई क्विज़ शुरू करें\n"
        "/score — अभी तक का स्कोर\n"
        "/start — शुरुआत में जाएं\n\n"
        "⏱️ हर सवाल का 30 सेकंड समय होता है\n"
        "💡 गलत जवाब पर ट्रिक मिलेगी!",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['quiz'])
def quiz(message):
    user_id = message.from_user.id
    questions = get_random_questions()
    user_sessions[user_id] = {
        "questions": questions,
        "current": 0,
        "score": 0,
        "wrong": [],
        "chat_id": message.chat.id,
        "poll_ids": {}
    }
    bot.reply_to(message, "🚀 क्विज़ शुरू हो रही है! तैयार रहें...\n\n⏱️ हर सवाल 30 सेकंड का है!")
    time.sleep(1)
    send_next_question(user_id)

def send_next_question(user_id):
    session = user_sessions.get(user_id)
    if not session:
        return
    idx = session["current"]
    questions = session["questions"]
    if idx >= len(questions):
        show_result(user_id)
        return
    q = questions[idx]
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
    question_text = f"{emoji} *प्रश्न {idx+1}/25* | {q['topic']}\n\n{q['q']}"
    sent = bot.send_poll(
        chat_id=session["chat_id"],
        question=question_text[:255],
        options=q["opts"],
        type="quiz",
        correct_option_id=q["ans"],
        explanation=f"✅ सही उत्तर!\n💡 ट्रिक: {q['trick']}",
        is_anonymous=False,
        open_period=30
    )
    session["poll_ids"][sent.poll.id] = user_id

@bot.poll_answer_handler()
def handle_answer(poll_answer):
    poll_id = poll_answer.poll_id
    user_id = poll_answer.user.id
    session = user_sessions.get(user_id)
    if not session:
        return
    idx = session["current"]
    questions = session["questions"]
    if idx >= len(questions):
        return
    q = questions[idx]
    selected = poll_answer.option_ids[0] if poll_answer.option_ids else -1
    if selected == q["ans"]:
        session["score"] += 1
    else:
        session["wrong"].append(q)
    session["current"] += 1
    time.sleep(2)
    send_next_question(user_id)

def show_result(user_id):
    session = user_sessions.get(user_id)
    if not session:
        return
    score = session["score"]
    total = len(session["questions"])
    pct = round(score / total * 100)
    if pct >= 80:
        grade = "🏆 उत्कृष्ट! आप प्रतिभाशाली हैं!"
    elif pct >= 60:
        grade = "👍 बहुत अच्छे! थोड़ी और मेहनत करें।"
    elif pct >= 40:
        grade = "📚 ठीक है! अभ्यास जारी रखें।"
    else:
        grade = "💪 हिम्मत रखें! जरूर सुधार होगा।"
    result = (
        f"🎉 *क्विज़ पूरी हुई!*\n\n"
        f"✅ सही उत्तर: *{score}/{total}*\n"
        f"📊 प्रतिशत: *{pct}%*\n"
        f"🎯 {grade}\n\n"
    )
    if session["wrong"]:
        result += "❌ *गलत उत्तरों की याददाश्त ट्रिक्स:*\n\n"
        for i, q in enumerate(session["wrong"], 1):
            result += f"*Q{i}.* {q['q']}\n✅ सही: {q['opts'][q['ans']]}\n💡 ट्रिक: {q['trick']}\n\n"
    else:
        result += "🌟 *शाबाश! सभी उत्तर सही थे!*"
    result += "\n\n▶️ फिर खेलें: /quiz"
    bot.send_message(session["chat_id"], result, parse_mode="Markdown")

@bot.message_handler(commands=['score'])
def score_cmd(message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id)
    if not session:
        bot.reply_to(message, "पहले /quiz से क्विज़ शुरू करें!")
        return
    bot.reply_to(message,
        f"📊 *आपका स्कोर:*\n"
        f"✅ सही: {session['score']}/{session['current']}",
        parse_mode="Markdown"
    )

print("✅ Bot चालू हो गया!")
bot.infinity_polling()
