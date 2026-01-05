# -*- coding: utf-8 -*-

import random
from docx import Document
from telegram.ext import Updater, CommandHandler, PollAnswerHandler

import os
TOKEN = os.environ.get("5863926239:AAFMIoGrSOpKxden0UwpPY7S4gRyVb5gD7U")
QUESTIONS_PER_TEST = 30

users = {}

def load_questions(filename):
    doc = Document(filename)
    questions = []

    q = None
    opts = []
    correct = None

    for p in doc.paragraphs:
        for line in p.text.splitlines():
            t = line.strip()
            if not t:
                continue

            if t.startswith("*"):
                if q and len(opts) >= 2 and correct is not None:
                    questions.append({"q": q, "opts": opts, "c": correct})
                q = t[1:].strip()
                opts = []
                correct = None

            elif t.startswith("+"):
                opts.append(t[1:].strip())
                correct = len(opts) - 1

            elif t.startswith("="):
                opts.append(t[1:].strip())

    if q and len(opts) >= 2 and correct is not None:
        questions.append({"q": q, "opts": opts, "c": correct})

    return questions


FAN1 = load_questions("yer osti yakuniy test.docx")
FAN2 = load_questions("maxsus fan yakuniy test.docx")

print("Yuklangan savollar:", len(FAN1), len(FAN2))


def start(update, context):
    update.message.reply_text(
        "✅ BOT ISHLAYAPTI\n\n"
        "/fan1 – Yer osti konchilik\n"
        "/fan2 – Maxsus fan"
    )


def start_test(update, context, bank):
    uid = update.effective_user.id
    users[uid] = {
        "qs": random.sample(bank, QUESTIONS_PER_TEST),
        "i": 0,
        "score": 0
    }
    send_question(uid, context)


def send_question(uid, context):
    data = users.get(uid)

    if data["i"] >= QUESTIONS_PER_TEST:
        context.bot.send_message(
            chat_id=uid,
            text=f"✅ Test tugadi!\nNatija: {data['score']} / {QUESTIONS_PER_TEST}"
        )
        users.pop(uid, None)
        return

    q = data["qs"][data["i"]]

    indexed = list(enumerate(q["opts"]))
    random.shuffle(indexed)

    options = [x[1] for x in indexed]
    correct = [i for i, x in enumerate(indexed) if x[0] == q["c"]][0]

    data["correct"] = correct
    data["i"] += 1

    context.bot.send_poll(
        chat_id=uid,
        question=f"[{data['i']}/{QUESTIONS_PER_TEST}] {q['q']}",
        options=options,
        type="quiz",
        correct_option_id=correct,
        is_anonymous=False
    )


def on_poll_answer(update, context):
    uid = update.poll_answer.user.id
    data = users.get(uid)

    if not data:
        return

    if update.poll_answer.option_ids:
        if update.poll_answer.option_ids[0] == data["correct"]:
            data["score"] += 1

    send_question(uid, context)


def fan1(update, context):
    start_test(update, context, FAN1)


def fan2(update, context):
    start_test(update, context, FAN2)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fan1", fan1))
    dp.add_handler(CommandHandler("fan2", fan2))
    dp.add_handler(PollAnswerHandler(on_poll_answer))

    updater.start_polling()
    print("BOT ISHLAYAPTI")
    updater.idle()


if __name__ == "__main__":
    main()
print("BOT RESTART CHECK")
