from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()


API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Подключаемся к базе данных SQLite
connection = sqlite3.connect('kbtu.db')
cursor = connection.cursor()

# Создаем таблицу, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        role TEXT NOT NULL
    )
''')
connection.commit()

schools = {
    "energy": "Школа энергетики и нефтегазовой индустрии",
    "geology": "Школа геологии",
    "it_engineering": "Школа информационных технологий и инженерии",
    "business": "Бизнес школа"
}

programs = {
    "energy": {
        "bachelor": (
            "*Программы бакалавриата Школы энергетики и нефтегазовой индустрии:*\n\n"
            "   *Описание:* Основной целью образовательной программы «Нефтегазовое дело» является подготовка конкурентоспособных и высококвалифицированных специалистов в нефтегазовой отрасли, занимающихся разработкой, добычей и эффективным использованием нефтяных и газовых месторождений и обладающих профессиональными и социальными компетенциями, отвечающими требованиям современной экономики и рынка труда."
            "1. *6B07201 — Нефтегазовое дело*\n"
            "   *Срок обучения:* 4-летнее обучение.\n\n"
            
            "2. *6B07201 — Нефтегазовое дело (для студентов колледжей АРЕС)*\n"
            "   *Срок обучения:* 2 года.\n\n"
            
            "3. *6B07201 — Нефтегазовое дело (двойной диплом с Китайским нефтяным университетом)*\n"
            "   *Срок обучения:* Двухдипломное обучение.\n"
        ),
        "master": (
            "*Программы магистратуры Школы энергетики и нефтегазовой индустрии:*\n\n"
            "1. *7M07201 — Нефтегазовое дело*\n"
            "   *Описание:* Программа направлена на подготовку магистров в области разработки и эксплуатации нефтяных и газовых месторождений, бурения и обслуживания нефтяных и газовых скважин. Программа включает современные теории и методы исследований для устойчивого развития нефтегазовой промышленности, повышения эффективности работы с труднодоступными запасами, моделирования процессов разработки месторождений, а также навыки рационального использования ресурсов.\n"
            "   *Срок обучения:* 1,5 и 2 года обучения.\n\n"
            
            "2. *7M07204 — Энергетический переход*\n"
            "   *Описание:* Программа подготовки специалистов в области энергетического перехода, нацеленная на удовлетворение современных требований энергетической индустрии. Включает изучение перехода от ископаемых топлив к возобновляемым источникам энергии, вопросы углеродной нейтральности, международные обязательства и риски, связанные с энергетическим переходом. В рамках программы рассматриваются технологии и материалы, востребованные для возобновляемой энергетики.\n"
            "   *Срок обучения:* 2-летнее исследование.\n\n"
            
            "3. *7M07203 — Управление промышленными проектами и инжиниринг*\n"
            "   *Описание:* Программа реализуется совместно с Agip Karachaganak B.V. и Eni Corporate University. Она направлена на подготовку инженеров-управленцев с базовыми знаниями управления проектами. Магистранты получают актуальные знания и опыт от руководителей и специалистов в нефтегазовой индустрии. Программа включает кейсы и прикладные задачи, преподаваемые приглашенными экспертами.\n"
            "   *Срок обучения:* 1,5 года обучения.\n"
        ),
        "doctorate": (
            "*Программы докторантуры Школы энергетики и нефтегазовой индустрии:*\n\n"
            "1. *8D07201 — Нефтегазовое дело*\n"
            "   *Описание:* Целью программы PhD «Нефтегазовое дело» является расширение знаний и опыта в области разведки, добычи и использования нефтяных ресурсов. Посредством тщательных исследований и академических исследований программа направлена на подготовку высококвалифицированных специалистов, способных решать сложные проблемы в нефтяной промышленности, способствовать инновациям и способствовать устойчивой и эффективной энергетической практике.\n"
            "   *Срок обучения:* 3-летнее обучение.\n\n"
            "   *Особенности:* Двухдипломное обучение с университетом Роберта Гордона (RGU) в формате 2+2 (PhD+EngD).\n"
        )
    },

    "geology": {
        "bachelor": (
            "*Бакалавриат Школы геологии*\n\n"
            "*Продолжительность обучения:* Образовательная программа бакалавриата Школы геологии по специальности 5B070600 — «Геология и разведка месторождений полезных ископаемых» рассчитана на 4 года с освоением не менее 140 кредитов.\n\n"
            "*Направления специализации:*\n"
            "- Геология и разведка месторождений твердых полезных ископаемых\n"
            "- Геология нефти и газа\n"
            "- Геоинформатика (по направлению Геофизические методы поисков и разведки месторождений полезных ископаемых)\n\n"
            "Программа включает в себя циклы фундаментальных дисциплин, таких как геодинамика и тектоника, геология месторождений полезных ископаемых, геология нефти и газа, промышленные типы месторождений полезных ископаемых, минералогия с основами кристаллографии и петрографии, промысловая геология, сейсморазведка, геоинформационные системы, принципы программирования и другие дисциплины, соответствующие выбранной специализации.\n\n"
            "Профессорско-преподавательский состав имеет многолетний опыт преподавания, а также опыт работы в ведущих производственных организациях.\n\n"
            "*Профессиональные навыки и подготовка:*\n"
            "Выпускники программы получают знания и навыки работы с программным обеспечением таких компаний, как Schlumberger, Halliburton, Baker Hughes, Rock Flow Dynamics, Emerson и других ведущих производителей. Это позволяет выпускникам планировать поисково-разведочные работы, обрабатывать и интерпретировать геолого-геофизические материалы, строить геолого-гидродинамические модели месторождений.\n\n"
            "Студенты также имеют возможность участвовать в программах академической мобильности, проходить стажировки в вузах ближнего и дальнего зарубежья, а также в производственных и недропользовательских компаниях.\n\n"
            "*Итоговая квалификация:* По результатам защиты дипломного проекта выпускникам присваивается степень Бакалавра техники и технологии по специальности «Геология и разведка месторождений полезных ископаемых».\n"
        ),
        "master": (
            "*Магистратура Школы геологии*\n\n"
            "Школа Геологии осуществляет подготовку кадров для высокотехнологичных и наукоемких производств в геологии, нефтегазовой отрасли, горнодобывающей промышленности, отвечающих требованиям современного рынка и международным стандартам.\n\n"
            "*Образовательная программа магистратуры* по специальности «Геология и разведка месторождений полезных ископаемых» рассчитана на 2 года и ориентирована на научно-педагогическое направление.\n\n"
            "*Направления подготовки:*\n"
            "- Геология и разведка твердых полезных ископаемых\n"
            "- Геология и разведка углеводородного сырья\n\n"
            "Программа нацелена на подготовку специалистов, которые смогут управлять и вести работы по поискам и разведке полезных ископаемых, а также на развитие исследовательских навыков и знаний для поддержки промышленности с учетом экономической и экологической безопасности при проведении поисково-разведочных работ добычи минерального сырья.\n\n"
            "Гибкая программа позволяет выбирать дисциплины по профилю, работать с высококвалифицированным профессорско-преподавательским составом и использовать лаборатории для научных исследований, тесно связанных с организациями геологической, нефтегазовой и горнодобывающей промышленности.\n\n"
            "*Обучение по специальности «Геология и разведка месторождений полезных ископаемых» включает:*\n"
            "- Высококвалифицированный профессорско-преподавательский состав;\n"
            "- Обучение с использованием инновационных методов, современного оборудования и программного обеспечения;\n"
            "- Высокий спрос на выпускников в Казахстане и за его пределами;\n"
            "- Тесное сотрудничество с компаниями-недропользователями, совместная подготовка кадров;\n"
            "- Признание качества обучения, подтвержденное успехами студентов и выпускников.\n"
        ),
        "doctorate": (
            "*Докторантура Школы геологии*\n\n"
            "*Образовательная программа докторантуры* по специальности «Геология и разведка месторождений полезных ископаемых» включает специализацию «Общая и региональная геология».\n\n"
            "*Цель программы:* Подготовка научных и научно-педагогических кадров для геологической и нефтегазовой отраслей Казахстана.\n\n"
            "Программа предназначена для подготовки докторов PhD по образовательной программе «Геология и разведка месторождений полезных ископаемых» в рамках направления «Производственные и обрабатывающие отрасли».\n\n"
            "Целью является достижение высокого качества профессиональной подготовки при соблюдении обязательных требований и уровня подготовки докторантов, что стимулирует их самостоятельную учебную, исследовательскую и профессиональную деятельность.\n\n"
            "*Особенности программы:* Докторантура предполагает фундаментальное образовательное, методологическое и исследовательское обучение, с углубленным изучением дисциплин по соответствующим направлениям для будущей научной и профессиональной деятельности в геологической сфере.\n"
        )
    },
    "it_engineering": {
         "bachelor": (
            "*Бакалавриат Школы информационных технологий и инженерии*\n\n"
            "1. *Автоматизация и управление*\n"
            "   Программа готовит инженеров с прочной инженерной базой в области автоматизации и управления, "
            "способных к анализу, синтезу и решению сложных технических задач. Выпускники становятся "
            "специалистами в разработке и внедрении автоматизированных систем управления, а также могут "
            "занимать руководящие роли в проектах.\n\n"
            
            "2. *Информационные системы (ИС)*\n"
            "   Программа ориентирована на подготовку специалистов с компетенциями в области информационных систем, "
            "которые умеют разрабатывать и внедрять информационные системы для различных секторов экономики. "
            "Выпускники способны профессионально внедрять ИС, интегрировать их в бизнес-процессы и разрабатывать "
            "инновационные решения для оптимизации данных и процессов.\n\n"
            
            "3. *Вычислительная техника и программное обеспечение (ВТиПО)*\n"
            "   Данная программа нацелена на подготовку профессионалов в области разработки программного обеспечения "
            "и вычислительных систем. Студенты осваивают как теоретические основы, так и практические навыки в "
            "программировании и проектировании ПО, что позволяет им работать над сложными задачами в различных "
            "областях промышленности.\n\n"
            
            "4. *Менеджмент в ИТ*\n"
            "   Программа фокусируется на подготовке специалистов в сфере IT-менеджмента, способных управлять "
            "IT-проектами и процессами. Обучение охватывает управление информационными системами и развитие "
            "организаций с акцентом на IT-решения и оптимизацию бизнес-процессов с помощью технологий.\n\n"
            
            "5. *Робототехника и мехатроника*\n"
            "   Программа обучает будущих инженеров по робототехнике и мехатронике, с акцентом на проектирование, "
            "программирование и управление робототехническими системами. Выпускники способны разрабатывать и "
            "внедрять робототехнические решения для промышленности и исследовать их интеграцию в производственные процессы.\n"
        ),
        "master": (
            "*Магистратура Школы информационных технологий и инженерии*\n\n"
            "Школа информационных технологий и инженерии предлагает восемь магистерских программ:\n"
            "1. 7M06105 \"Наука о данных\"\n"
            "2. 7M06104 \"ИТ менеджмент\"\n"
            "3. 7M06106 \"Программная инженерия\"\n"
            "4. 7M06107 \"Компьютерные науки и аналитика данных\"\n"
            "5. 7M06101 \"Информационные системы\"\n"
            "6. 7M07106 \"Промышленная и системная инженерия\"\n"
            "7. 7M07125 \"Электроника и системы управления\"\n"
            "8. 7M07105 \"Умные города и умные системы\"\n\n"
            
            "Программы для магистрантов сосредоточены на развитии навыков и знаний, необходимых для успешной карьеры в IT, "
            "включая разработку программного обеспечения, науку о данных, управление IT, кибербезопасность и компьютерные науки.\n\n"
            "*Язык преподавания*: Английский.\n"
            "Продолжительность обучения составляет 1,5–2 года, в зависимости от направления программы.\n"
        ),
        "doctorate": (
            "*Программы докторантуры Школы информационных технологий и инженерии*\n\n"
            "Школа информационных технологий и инженерии предлагает две программы PhD:\n"
            "1. 8D06101 \"Информатика, вычислительная техника и управление\"\n"
            "2. 8D06102 \"Компьютерная наука и искусственный интеллект\"\n\n"
            
            "Программа PhD ориентирована на подготовку высококвалифицированных научных и научно-педагогических кадров для деятельности, "
            "требующей углубленной фундаментальной и профессиональной подготовки и знаний в области информатики и вычислительной техники.\n\n"
            "Программы ориентированы на тех, кто хочет создать новые более эффективные методы обработки и накопления информации, "
            "новые методы и средства интеллектуальной обработки данных, инструментальные и прикладные программные системы различных классов "
            "для автоматизации профессиональной деятельности в различных предметных областях и для решения различных новых классов задач.\n\n"
            "*Язык преподавания*: Английский.\n"
            "Продолжительность обучения составляет 3 года.\n"
        )
    },
    "business": {
        "bachelor": (
            "*Бакалавриат Бизнес школы*\n\n"
            # Здесь добавьте информацию для бакалавриата
        ),
        "master": (
            "*Магистратура Бизнес школы*\n\n"
            # Здесь добавьте информацию для магистратуры
        ),
        "doctorate": (
            "*Программы докторантуры Бизнес школы*\n\n"
            # Здесь добавьте информацию для докторантуры
        )
    }
    # Добавьте информацию для других школ
}

# Определяем состояния для FSM
class RoleState(StatesGroup):
    waiting_for_role = State()
    changing_role = State()

def get_user_role(user_id):
    """Проверяет существование пользователя в базе данных и возвращает его роль, если она есть."""
    cursor.execute("SELECT role FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

@dp.message(Command('start'))
async def send_welcome(message: Message, state: FSMContext):
    user_id = message.from_user.id
    role = get_user_role(user_id)

    if role == "Студент":
        # Список команд для студента
        commands = (
            "/events — Студенческие мероприятия\n"
            "/contact — Поддержка студентов\n"
            "/schedule — Расписание занятий\n"
            "/grades — Оценки и успеваемость\n"
            "/library — Библиотека\n"
            "/change_role — Изменить роль"
        )
    elif role == "Абитуриент":
        # Список команд для абитуриента
        commands = (
            "/faculties — Информация о факультетах\n"
            "/admission — Правила поступления\n"
            "/tuition — Стоимость обучения\n"
            "/dormitory — Общежитие\n"
            "/contact — Контактная информация\n"
            "/change_role — Изменить роль"
        )
    else:
        # Если роль не определена, предлагаем зарегистрироваться
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Студент", callback_data="role_Студент"),
                    InlineKeyboardButton(text="Абитуриент", callback_data="role_Абитуриент")
                ]
            ]
        )
        await message.reply("Вы не зарегистрированы. Пожалуйста, выберите вашу роль:", reply_markup=keyboard)
        await state.set_state(RoleState.waiting_for_role)
        return

    # Отправляем список команд в зависимости от роли
    await message.reply(f"Добро пожаловать, {role}!\nВот список доступных команд:\n\n{commands}")
@dp.callback_query(lambda c: c.data and c.data.startswith('role_'))
async def process_role(callback_query: CallbackQuery, state: FSMContext):
    role = callback_query.data.split('_')[1]

    # Сохраняем пользователя в базу данных
    user_id = callback_query.from_user.id
    cursor.execute("INSERT OR REPLACE INTO users (id, role) VALUES (?, ?)", (user_id, role))
    connection.commit()

    # Подтверждаем регистрацию и убираем inline-клавиатуру
    await callback_query.message.edit_text(f"Спасибо! Ваша роль '{role}' сохранена.")
    await state.clear()

@dp.message(Command('change_role'))
async def change_role(message: Message, state: FSMContext):
    user_id = message.from_user.id
    role = get_user_role(user_id)

    if role:
        # Если пользователь найден, предлагаем ему изменить роль
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Студент", callback_data="change_role_Студент"),
                    InlineKeyboardButton(text="Абитуриент", callback_data="change_role_Абитуриент")
                ]
            ]
        )
        await message.reply("Выберите вашу новую роль:", reply_markup=keyboard)
        await state.set_state(RoleState.changing_role)
    else:
        # Если пользователя нет в базе, сообщаем ему, что сначала нужно зарегистрироваться
        await message.reply("Вы еще не зарегистрированы. Пожалуйста, используйте команду /start для регистрации.")

@dp.callback_query(lambda c: c.data and c.data.startswith('change_role_'))
async def process_role_change(callback_query: CallbackQuery, state: FSMContext):
    new_role = callback_query.data.split('_')[2]

    # Обновляем роль пользователя в базе данных
    user_id = callback_query.from_user.id
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    connection.commit()

    # Подтверждаем изменение роли и убираем inline-клавиатуру
    await callback_query.message.edit_text(f"Ваша роль изменена на '{new_role}'.")
    await state.clear()



@dp.message(Command('faculties'))
async def show_schools(message: types.Message):
    # Создаем клавиатуру для школ
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=value, callback_data=f"school_{key}")]
        for key, value in schools.items()
    ])
    
    await message.reply("Выберите школу:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data and c.data.startswith('school_'))
async def show_levels(callback_query: CallbackQuery):
    school_key = callback_query.data.split('_')[1]

    # Создаем клавиатуру для выбора уровня обучения
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Бакалавриат", callback_data=f"level_{school_key}_bachelor")],
        [InlineKeyboardButton(text="Магистратура", callback_data=f"level_{school_key}_master")],
        [InlineKeyboardButton(text="Докторантура", callback_data=f"level_{school_key}_doctorate")]
    ])

    await callback_query.message.edit_text("Выберите уровень обучения:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data and c.data.startswith('level_'))
async def show_programs(callback_query: CallbackQuery):
    _, school_key, level = callback_query.data.split('_')

    # Получаем текст программ для выбранного уровня и школы
    text = programs.get(school_key, {}).get(level, "Информация отсутствует.")

    await callback_query.message.edit_text(text, parse_mode="Markdown")


@dp.message(Command('admission'))
async def admission_requirements(message: types.Message):
    text = (
        "*Список необходимых документов для поступления*\n\n"
        "1\\. *Заявление*\n"
        "   *Тип:* Онлайн\n"
        "   *Инструкция:* [Скачать шаблон заявления](https://drive.google.com/file/d/11bKZzg2kCIxLjK3mdZ8BGxHkuBz-U7gG/view)\\. Заполненное заявление прикрепите через личный кабинет абитуриента\\.\n\n"
        
        "2\\. *Удостоверение личности*\n"
        "   *Тип:* Копия\n"
        "   *Инструкция:* Сделайте копию удостоверения личности и загрузите её в личный кабинет\\.\n\n"
        
        "3\\. *Анкета абитуриента*\n"
        "   *Тип:* Онлайн\n"
        "   *Инструкция:* Анкета заполняется онлайн в личном кабинете абитуриента\\.\n\n"
        
        "4\\. *Аттестат и приложение \\(для выпускников школ\\) / Диплом и приложение \\(для выпускников колледжей\\)*\n"
        "   *Тип:* Оригинал\n"
        "   *Инструкция:* Оригинал предоставляется при подаче документов лично в приёмной комиссии\\.\n\n"
        
        "5\\. *Сертификат ЕНТ* \\(всем, кроме выпускников APEC PetroTechnic и программ МШЭ без ЕНТ\\)\n"
        "   *Тип:* Распечатка из личного кабинета НЦТ\n"
        "   *Инструкция:* Распечатайте сертификат ЕНТ и прикрепите его в личном кабинете\\.\n\n"
        
        "6\\. *Сертификат по английскому языку* \\(IELTS 5\\.5 / TOEFL iBT 46 / STEP Intermediate\\)\n"
        "   *Тип:* Копия\n"
        "   *Инструкция:* Загрузите копию сертификата в личный кабинет, если требуется\\.\n\n"
        
        "7\\. *Фотография 3x4*\n"
        "   *Тип:* Оригинал \\(1 шт\\.\\)\n"
        "   *Инструкция:* Фотографию можно загрузить онлайн в формате JPEG\\.\n\n"
        
        "8\\. *Снимок флюорографии*\n"
        "   *Тип:* Оригинал, действителен 1 год\n"
        "   *Инструкция:* Снимок предоставляется лично при подаче документов\\.\n\n"
        
        "9\\. *Медицинская справка №075\\-У*\n"
        "   *Тип:* Оригинал, действителен 6 месяцев\n"
        "   *Инструкция:* Оригинал предоставляется при подаче документов лично\\.\n\n"
        
        "10\\. *Форма 063/у \\(прививочная карта\\)*\n"
        "    *Тип:* Копия\n"
        "    *Инструкция:* Копия загружается в личный кабинет\\.\n\n"
        
        "11\\. *Приписное свидетельство / Справка из военкомата* \\(для юношей\\)\n"
        "    *Тип:* Копия\n"
        "    *Инструкция:* Загрузите копию документа в личный кабинет\\.\n\n"
        
        "12\\. *Мотивационное письмо*\n"
        "    *Тип:* Онлайн\n"
        "    *Инструкция:* Письмо загружается в электронном виде через личный кабинет\\.\n\n"
        
        "13\\. *Договор на обучение*\n"
        "    *Тип:* Электронный\n"
        "    *Инструкция:* Подписанный договор прикрепите онлайн\\.\n\n"
        
        "14\\. *Документы, подтверждающие социальную категорию \\(для льгот / скидки КБТУ\\)*\n"
        "    *Тип:* Копия\n"
        "    *Инструкция:* Загрузите копии подтверждающих документов в личный кабинет\\. [Список документов по квотам](https://drive.google.com/file/d/1fIXBRAdkIRW7hhyOW8dbLf9FemwxTiZQ/view?usp=sharing)\\.\n\n"
        
        "15\\. *Чек об оплате вступительного взноса*\n"
        "    *Тип:* Распечатанный чек из Kaspi\n"
        "    *Инструкция:* Загрузите чек в личный кабинет\\.\n\n"
        
        "16\\. *Чек об оплате Student Fee*\n"
        "    *Тип:* Распечатанный чек из Halyk Bank\n"
        "    *Инструкция:* Загрузите чек в личный кабинет\\.\n"
    )
    
    await message.reply(text, parse_mode="MarkdownV2")

@dp.message(Command('tuition'))
async def tuition_info(message: types.Message):
    text = (
        "*Информация о стоимости обучения*\n\n"
        "Для получения полной информации о стоимости обучения в КБТУ, пожалуйста, ознакомьтесь с документом по следующей ссылке:\n"
        "[Скачать информацию о стоимости обучения](https://drive.google.com/file/d/1fIXBRAdkIRW7hhyOW8dbLf9FemwxTiZQ/view?usp=sharing)"
    )
    
    await message.reply(text, parse_mode="MarkdownV2")

@dp.message(Command('dormitory'))
async def dormitory_info(message: types.Message):
    text = (
        "*Общежитие KBTU JASTAR CITY*\n\n"
        "KBTU JASTAR CITY — это общежитие нового поколения, состоящее из 5 корпусов, с комфортными 1-, 2-, 3- и 4-местными комнатами. "
        "Общежитие оборудовано всем необходимым для жизни, учебы и отдыха, включая стиральные машины, гладильные доски и библиотеку. "
        "Ежегодно проводятся работы по обновлению мебели и бытовой техники.\n\n"
        
        "*Инфраструктура*: Жилой комплекс окружен развитой инфраструктурой — рядом находятся магазины, аптеки и остановки. "
        "В общежитии также работают столовая и буфет, доступен Service Desk для реагирования на запросы студентов.\n\n"
        
        "*Студенческий совет и досуг*: В общежитии функционирует Студенческий совет, организующий мероприятия и решающий вопросы проживания. "
        "Проводятся лекции, спортивные соревнования, киберспортивные турниры и субботники.\n\n"
        
        "*Медицинская помощь и безопасность*: В общежитии предусмотрены медицинские кабинеты и изолятор для инфекционных больных. "
        "Установлены камеры видеонаблюдения, система пропусков с Face-ID и доступ в общежитие через турникеты.\n\n"
        
        "*Стоимость проживания в KBTU JASTAR CITY на 2024-2025 учебный год*\n\n"
        "Корпуса №1, 2, 5 (студенты 2-4 курсов, магистранты, иностранные студенты)\n"
        "1-местная комната: 60 000 KZT\n"
        "2-местная комната: 50 000 KZT\n"
        "3-местная комната: 45 000 KZT\n"
        "4-местная комната: 40 000 KZT\n\n"
        
        "Корпуса №3, 4 (студенты первого курса)\n"
        "3-местная комната: 55 000 KZT\n"
        "4-местная комната: 50 000 KZT\n\n"
        
        "*Социальные льготы*\n\n"
        "Дети-сироты: Бесплатно\n"
        "Сироты под опекой: Бесплатно\n"
        "Студенты-инвалиды, не проживающие в комнатах МГН: 50%\n"
    )

    await message.reply(text, parse_mode="Markdown")


@dp.message(Command('contact'))
async def contact_info(message: types.Message):
    text = (
        "*Контактная информация:*\n\n"
        "📞 *Call-центр*: +7 (727) 357 42 42\n"
        "📧 *Служба поддержки студентов*: [helpdesk@kbtu.kz](mailto:helpdesk@kbtu.kz)\n\n"
        
        "📞 *Call-центр общежития*: +7 (727) 357 42 12\n"
        "📧 *Для корреспонденции*: [kense@kbtu.kz](mailto:kense@kbtu.kz)\n"
    )

    await message.reply(text, parse_mode="Markdown")



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    connection.close()

