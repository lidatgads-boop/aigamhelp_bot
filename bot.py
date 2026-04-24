import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

# ──────────────────────────────────────────────
# Состояния викторины
# ──────────────────────────────────────────────
QUIZ_GENRE, QUIZ_TIME, QUIZ_PLATFORM, QUIZ_MOOD = range(4)

# ──────────────────────────────────────────────
# Главное меню
# ──────────────────────────────────────────────
MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Подобрать игру")],
        [KeyboardButton("Обзоры игр"), KeyboardButton("Гайды")],
        [KeyboardButton("Что умеет бот"), KeyboardButton("О проекте")],
        [KeyboardButton("Контакты")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)


# ──────────────────────────────────────────────
# /start
# ──────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    text = (
        "Добро пожаловать в GameMatch — бот для подбора видеоигр.\n\n"
        "Здесь вы найдёте:\n"
        "• персональные рекомендации игр\n"
        "• обзоры популярных новинок\n"
        "• гайды и советы для разных жанров\n\n"
        "Воспользуйтесь меню ниже для навигации."
    )
    await update.message.reply_text(text, reply_markup=MAIN_MENU_KEYBOARD)


# ──────────────────────────────────────────────
# Раздел: Что умеет бот
# ──────────────────────────────────────────────
async def about_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "GameMatch умеет:\n\n"
        "Подбор игр — ответьте на 4 вопроса и получите персональную подборку, "
        "составленную с учётом вашего жанра, платформы и настроения.\n\n"
        "Обзоры — краткие честные обзоры актуальных игр с оценками по ключевым критериям.\n\n"
        "Гайды — полезные советы по популярным играм: прохождение, механики, секреты.\n\n"
        "Поиск — введите название игры, и бот покажет основную информацию о ней.\n\n"
        "Все разделы доступны через меню."
    )
    await update.message.reply_text(text, reply_markup=MAIN_MENU_KEYBOARD)


# ──────────────────────────────────────────────
# Раздел: О проекте
# ──────────────────────────────────────────────
async def about_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "GameMatch — независимый проект для игрового сообщества.\n\n"
        "Наша цель — помочь вам находить игры, которые действительно подходят "
        "именно вам, а не теряться в тысячах релизов.\n\n"
        "Мы регулярно обновляем базу обзоров и гайдов, добавляем новые игры "
        "и совершенствуем алгоритм подбора.\n\n"
        "Бот находится в активной разработке — ваши отзывы помогают делать его лучше."
    )
    await update.message.reply_text(text, reply_markup=MAIN_MENU_KEYBOARD)


# ──────────────────────────────────────────────
# Раздел: Контакты
# ──────────────────────────────────────────────
async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Связь с командой GameMatch:\n\n"
        "Написать напрямую: @gamematch_support\n\n"
        "Мы отвечаем в будние дни с 10:00 до 20:00 (МСК).\n\n"
        "Предложения по улучшению бота, сотрудничество и вопросы — "
        "всё можно направить по указанному контакту."
    )
    await update.message.reply_text(text, reply_markup=MAIN_MENU_KEYBOARD)


# ──────────────────────────────────────────────
# Раздел: Обзоры
# ──────────────────────────────────────────────
REVIEWS = [
    {
        "title": "Elden Ring",
        "year": 2022,
        "genre": "Action RPG",
        "score": "9.5/10",
        "text": (
            "Открытый мир от FromSoftware стал событием года. "
            "Огромная карта, сотни боссов и глубокий лор делают игру "
            "одной из лучших в жанре. Высокий порог вхождения — это честное предупреждение."
        ),
        "pros": "Масштаб, свобода исследования, боссы",
        "cons": "Сложность может отпугнуть новичков",
    },
    {
        "title": "Baldur's Gate 3",
        "year": 2023,
        "genre": "RPG / Тактика",
        "score": "9.8/10",
        "text": (
            "Лучшая RPG последнего десятилетия. Невероятная глубина диалогов, "
            "тактические бои и кооператив на четырёх игроков. "
            "Десятки часов без ощущения пустоты."
        ),
        "pros": "Сюжет, вариативность, кооператив",
        "cons": "Требовательна к железу, долгое начало",
    },
    {
        "title": "Hades II",
        "year": 2024,
        "genre": "Roguelite / Action",
        "score": "9.2/10",
        "text": (
            "Продолжение культового рогалика от Supergiant. "
            "Новая героиня, обновлённая боевая система и ещё более "
            "насыщенный нарратив. Один из лучших представителей жанра."
        ),
        "pros": "Геймплейный цикл, музыка, нарратив",
        "cons": "Ранний доступ, часть контента ещё в разработке",
    },
]

async def reviews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{r['title']} ({r['score']})", callback_data=f"review_{i}")]
        for i, r in enumerate(REVIEWS)
    ])
    await update.message.reply_text(
        "Выберите игру для просмотра обзора:",
        reply_markup=keyboard,
    )

async def review_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idx = int(query.data.split("_")[1])
    r = REVIEWS[idx]
    text = (
        f"{r['title']} ({r['year']})\n"
        f"Жанр: {r['genre']}\n"
        f"Оценка: {r['score']}\n\n"
        f"{r['text']}\n\n"
        f"Плюсы: {r['pros']}\n"
        f"Минусы: {r['cons']}"
    )
    back_btn = InlineKeyboardMarkup([[InlineKeyboardButton("<- Назад к обзорам", callback_data="reviews_back")]])
    await query.edit_message_text(text, reply_markup=back_btn)

async def reviews_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{r['title']} ({r['score']})", callback_data=f"review_{i}")]
        for i, r in enumerate(REVIEWS)
    ])
    await query.edit_message_text("Выберите игру для просмотра обзора:", reply_markup=keyboard)


# ──────────────────────────────────────────────
# Раздел: Гайды
# ──────────────────────────────────────────────
GUIDES = {
    "Общие советы для новичков": (
        "1. Начинайте с игр, у которых есть обучение — оно сэкономит время.\n"
        "2. Не бойтесь менять сложность: игра должна приносить удовольствие, а не стресс.\n"
        "3. Читайте описания предметов и умений — большинство механик объяснены в самой игре.\n"
        "4. Делайте паузы: 1-2 часа в день комфортнее, чем многочасовые марафоны.\n"
        "5. Пробуйте жанры за пределами зоны комфорта — часто именно там находится любимая игра."
    ),
    "Как выбрать игру по жанру": (
        "Action / Экшен — для тех, кто хочет динамику и быстрые реакции.\n"
        "RPG — для любителей глубоких историй и развития персонажа.\n"
        "Стратегия — если нравится думать, планировать и управлять ресурсами.\n"
        "Инди — небольшие игры часто предлагают уникальный опыт за меньшие деньги.\n"
        "Roguelite — короткие забеги с нарастающей сложностью, идеально для ограниченного времени."
    ),
    "Советы по Elden Ring": (
        "1. Не спешите в основные локации — исследуйте катакомбы и подземелья для прокачки.\n"
        "2. Уровень кузнеца важнее уровня персонажа: улучшайте оружие.\n"
        "3. Призывайте духов в сложных боях — это не читерство, это механика игры.\n"
        "4. Торрент (лошадь) — ваш главный союзник в открытом мире.\n"
        "5. Читайте описания предметов: в них скрыт лор и подсказки."
    ),
}

async def guides(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(title, callback_data=f"guide_{i}")]
        for i, title in enumerate(GUIDES.keys())
    ])
    await update.message.reply_text("Выберите тему гайда:", reply_markup=keyboard)

async def guide_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    idx = int(query.data.split("_")[1])
    title = list(GUIDES.keys())[idx]
    text = f"{title}\n\n{GUIDES[title]}"
    back_btn = InlineKeyboardMarkup([[InlineKeyboardButton("<- Назад к гайдам", callback_data="guides_back")]])
    await query.edit_message_text(text, reply_markup=back_btn)

async def guides_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(title, callback_data=f"guide_{i}")]
        for i, title in enumerate(GUIDES.keys())
    ])
    await query.edit_message_text("Выберите тему гайда:", reply_markup=keyboard)


# ──────────────────────────────────────────────
# Викторина: Подбор игры
# ──────────────────────────────────────────────
RECOMMENDATIONS = {
    ("action", "short", "pc", "relax"):      ["Hades II", "Dead Cells", "Vampire Survivors"],
    ("action", "short", "pc", "serious"):    ["Sekiro", "Hollow Knight", "Returnal"],
    ("action", "long", "pc", "relax"):       ["God of War", "Spider-Man", "Cyberpunk 2077"],
    ("action", "long", "pc", "serious"):     ["Elden Ring", "Dark Souls III", "Nioh 2"],
    ("action", "short", "console", "relax"): ["Astro's Playroom", "Hades II", "Celeste"],
    ("action", "short", "console", "serious"):["Returnal", "Hollow Knight", "Dead Cells"],
    ("action", "long", "console", "relax"):  ["God of War Ragnarok", "Horizon FW", "Ratchet and Clank"],
    ("action", "long", "console", "serious"):["Elden Ring", "Sekiro", "Ghost of Tsushima"],
    ("rpg", "short", "pc", "relax"):         ["Disco Elysium", "Undertale", "Hades II"],
    ("rpg", "short", "pc", "serious"):       ["Planescape Torment", "Disco Elysium", "Tyranny"],
    ("rpg", "long", "pc", "relax"):          ["Baldurs Gate 3", "Divinity OS2", "The Witcher 3"],
    ("rpg", "long", "pc", "serious"):        ["Baldurs Gate 3", "Pathfinder WotR", "Dragon Age Origins"],
    ("rpg", "short", "console", "relax"):    ["Undertale", "CrossCode", "Octopath Traveler"],
    ("rpg", "short", "console", "serious"):  ["Octopath Traveler", "Crisis Core", "Xenogears"],
    ("rpg", "long", "console", "relax"):     ["The Witcher 3", "Final Fantasy XVI", "Persona 5"],
    ("rpg", "long", "console", "serious"):   ["Baldurs Gate 3", "Final Fantasy XIV", "Dragons Dogma 2"],
    ("strategy", "short", "pc", "relax"):    ["Into the Breach", "Slay the Spire", "FTL"],
    ("strategy", "short", "pc", "serious"):  ["XCOM 2", "Slay the Spire", "Dungeon of the Endless"],
    ("strategy", "long", "pc", "relax"):     ["Civilization VI", "Age of Empires IV", "Humankind"],
    ("strategy", "long", "pc", "serious"):   ["Total War Warhammer III", "Crusader Kings III", "Victoria 3"],
    ("strategy", "short", "console", "relax"):["Into the Breach", "FTL", "Slay the Spire"],
    ("strategy", "short", "console", "serious"):["XCOM 2", "Into the Breach", "Armello"],
    ("strategy", "long", "console", "relax"): ["Civilization VI", "Two Point Hospital", "Planet Coaster"],
    ("strategy", "long", "console", "serious"):["XCOM 2", "Frostpunk", "Ashes of the Singularity"],
    ("indie", "short", "pc", "relax"):       ["Stardew Valley", "Unpacking", "A Short Hike"],
    ("indie", "short", "pc", "serious"):     ["Celeste", "Disco Elysium", "Papers Please"],
    ("indie", "long", "pc", "relax"):        ["Stardew Valley", "Terraria", "Hollow Knight"],
    ("indie", "long", "pc", "serious"):      ["Hollow Knight", "Outer Wilds", "Disco Elysium"],
    ("indie", "short", "console", "relax"):  ["A Short Hike", "Unpacking", "Donut County"],
    ("indie", "short", "console", "serious"):["Celeste", "Inside", "Limbo"],
    ("indie", "long", "console", "relax"):   ["Stardew Valley", "Terraria", "My Time at Portia"],
    ("indie", "long", "console", "serious"): ["Hollow Knight", "Outer Wilds", "Spiritfarer"],
    ("action", "short", "mobile", "relax"):  ["Pascals Wager", "Oceanhorn", "Altos Odyssey"],
    ("action", "short", "mobile", "serious"):["Pascals Wager", "Grimvalor", "Hyperlight Drifter"],
    ("action", "long", "mobile", "relax"):   ["Genshin Impact", "Honkai Star Rail", "Oceanhorn 2"],
    ("action", "long", "mobile", "serious"): ["Genshin Impact", "Pascals Wager", "Diablo Immortal"],
    ("rpg", "short", "mobile", "relax"):     ["Stardew Valley Mobile", "Evoland", "Chrono Trigger"],
    ("rpg", "short", "mobile", "serious"):   ["Chrono Trigger", "FF Tactics", "80 Days"],
    ("rpg", "long", "mobile", "relax"):      ["Genshin Impact", "Honkai Star Rail", "AFK Arena"],
    ("rpg", "long", "mobile", "serious"):    ["Genshin Impact", "Diablo Immortal", "Star Ocean AC"],
    ("strategy", "short", "mobile", "relax"):["Mini Metro", "Polytopia", "Reigns"],
    ("strategy", "short", "mobile", "serious"):["Polytopia", "Bad North", "Into the Breach Mobile"],
    ("strategy", "long", "mobile", "relax"): ["Polytopia", "Civilization Revolution", "Tower Defense"],
    ("strategy", "long", "mobile", "serious"):["Polytopia", "Battle Brothers", "Darkest Dungeon Mobile"],
    ("indie", "short", "mobile", "relax"):   ["Altos Odyssey", "Monument Valley", "Donut County"],
    ("indie", "short", "mobile", "serious"): ["Papers Please", "Florence", "Inside"],
    ("indie", "long", "mobile", "relax"):    ["Stardew Valley", "Terraria Mobile", "Crashlands"],
    ("indie", "long", "mobile", "serious"):  ["Slay the Spire", "Dead Cells Mobile", "Hades Switch"],
}


async def quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quiz"] = {}
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Экшен / Боевик", callback_data="qg_action")],
        [InlineKeyboardButton("Ролевая игра (RPG)", callback_data="qg_rpg")],
        [InlineKeyboardButton("Стратегия", callback_data="qg_strategy")],
        [InlineKeyboardButton("Инди / Атмосферные", callback_data="qg_indie")],
    ])
    await update.message.reply_text(
        "Шаг 1 из 4. Какой жанр вам ближе?",
        reply_markup=keyboard,
    )
    return QUIZ_GENRE


async def quiz_genre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["quiz"]["genre"] = query.data.replace("qg_", "")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("До 5 часов (короткие сессии)", callback_data="qt_short")],
        [InlineKeyboardButton("20+ часов (глубокое погружение)", callback_data="qt_long")],
    ])
    await query.edit_message_text("Шаг 2 из 4. Сколько времени готовы уделить игре?", reply_markup=keyboard)
    return QUIZ_TIME


async def quiz_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["quiz"]["time"] = query.data.replace("qt_", "")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("PC (Steam / Epic)", callback_data="qp_pc")],
        [InlineKeyboardButton("Консоль (PS / Xbox / Switch)", callback_data="qp_console")],
        [InlineKeyboardButton("Мобильный (iOS / Android)", callback_data="qp_mobile")],
    ])
    await query.edit_message_text("Шаг 3 из 4. На какой платформе будете играть?", reply_markup=keyboard)
    return QUIZ_PLATFORM


async def quiz_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["quiz"]["platform"] = query.data.replace("qp_", "")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Хочу расслабиться и отдохнуть", callback_data="qm_relax")],
        [InlineKeyboardButton("Хочу бросить себе вызов", callback_data="qm_serious")],
    ])
    await query.edit_message_text("Шаг 4 из 4. Какое настроение сейчас?", reply_markup=keyboard)
    return QUIZ_MOOD


async def quiz_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["quiz"]["mood"] = query.data.replace("qm_", "")

    q = context.user_data["quiz"]
    key = (q["genre"], q["time"], q["platform"], q["mood"])
    games = RECOMMENDATIONS.get(key, ["The Witcher 3", "Stardew Valley", "Hades II"])

    genre_label = {"action": "Экшен", "rpg": "RPG", "strategy": "Стратегия", "indie": "Инди"}.get(q["genre"], q["genre"])
    time_label = "короткие сессии" if q["time"] == "short" else "долгое погружение"
    platform_label = {"pc": "PC", "console": "Консоль", "mobile": "Мобильный"}.get(q["platform"], q["platform"])
    mood_label = "отдых" if q["mood"] == "relax" else "вызов"

    text = (
        f"Подборка готова.\n\n"
        f"Ваш профиль: {genre_label}, {time_label}, {platform_label}, {mood_label}.\n\n"
        f"Рекомендуемые игры:\n"
        f"1. {games[0]}\n"
        f"2. {games[1]}\n"
        f"3. {games[2]}\n\n"
        f"Введите название любой из них в чате, чтобы узнать подробности, "
        f"или воспользуйтесь другими разделами меню."
    )
    await query.edit_message_text(text)
    return ConversationHandler.END


async def quiz_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Подбор игры отменён. Вы можете вернуться к нему в любой момент.",
        reply_markup=MAIN_MENU_KEYBOARD
    )
    return ConversationHandler.END


# ──────────────────────────────────────────────
# Поиск по названию игры
# ──────────────────────────────────────────────
GAME_DB = {
    "elden ring": {
        "full": "Elden Ring (2022) — Action RPG от FromSoftware и Джорджа Р. Р. Мартина. "
                "Огромный открытый мир, сотни уникальных боссов, глубокий лор. "
                "Подходит тем, кто готов к высокой сложности и исследованию.",
        "score": "9.5/10", "genre": "Action RPG", "platform": "PC, PS5, Xbox",
    },
    "baldurs gate 3": {
        "full": "Baldur's Gate 3 (2023) — RPG от Larian Studios на основе правил D&D 5e. "
                "Глубокий сюжет, тактические пошаговые бои, кооператив до 4 игроков.",
        "score": "9.8/10", "genre": "RPG / Тактика", "platform": "PC, PS5",
    },
    "hades": {
        "full": "Hades (2020) — roguelite от Supergiant Games. "
                "Быстрые забеги, исключительный нарратив, отличный саундтрек.",
        "score": "9.3/10", "genre": "Roguelite / Action", "platform": "PC, Switch, PS, Xbox",
    },
    "stardew valley": {
        "full": "Stardew Valley (2016) — симулятор фермы с элементами RPG. "
                "Расслабляющий темп, богатая социальная система, контент на сотни часов.",
        "score": "9.4/10", "genre": "Симулятор / Инди", "platform": "PC, Switch, PS, Xbox, Mobile",
    },
    "celeste": {
        "full": "Celeste (2018) — платформер с историей о борьбе с тревожностью. "
                "Сложный, но честный геймплей, трогательный сюжет, выдающийся саундтрек.",
        "score": "9.2/10", "genre": "Платформер / Инди", "platform": "PC, Switch, PS, Xbox",
    },
}

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_lower = update.message.text.lower().strip()

    # Обработка кнопок меню
    menu_handlers = {
        "подобрать игру": quiz_start,
        "обзоры игр": reviews,
        "гайды": guides,
        "что умеет бот": about_bot,
        "о проекте": about_company,
        "контакты": contacts,
    }
    for key, handler in menu_handlers.items():
        if text_lower == key:
            return await handler(update, context)

    # Поиск игры по названию
    for game_key, info in GAME_DB.items():
        if game_key in text_lower or text_lower in game_key:
            reply = (
                f"Игра найдена.\n\n"
                f"{info['full']}\n\n"
                f"Жанр: {info['genre']}\n"
                f"Платформы: {info['platform']}\n"
                f"Оценка: {info['score']}"
            )
            await update.message.reply_text(reply, reply_markup=MAIN_MENU_KEYBOARD)
            return

    await update.message.reply_text(
        "Введите название игры точнее, или воспользуйтесь разделами меню.",
        reply_markup=MAIN_MENU_KEYBOARD,
    )


# ──────────────────────────────────────────────
# Запуск
# ──────────────────────────────────────────────
def main():
    app = Application.builder().token(TOKEN).build()

    quiz_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Подобрать игру$"), quiz_start)],
        states={
            QUIZ_GENRE:    [CallbackQueryHandler(quiz_genre,    pattern="^qg_")],
            QUIZ_TIME:     [CallbackQueryHandler(quiz_time,     pattern="^qt_")],
            QUIZ_PLATFORM: [CallbackQueryHandler(quiz_platform, pattern="^qp_")],
            QUIZ_MOOD:     [CallbackQueryHandler(quiz_mood,     pattern="^qm_")],
        },
        fallbacks=[CommandHandler("cancel", quiz_cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(quiz_handler)
    app.add_handler(CallbackQueryHandler(review_detail,  pattern="^review_\\d+$"))
    app.add_handler(CallbackQueryHandler(reviews_back,   pattern="^reviews_back$"))
    app.add_handler(CallbackQueryHandler(guide_detail,   pattern="^guide_\\d+$"))
    app.add_handler(CallbackQueryHandler(guides_back,    pattern="^guides_back$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Бот запущен.")
    app.run_polling()


if __name__ == "__main__":
    main()
