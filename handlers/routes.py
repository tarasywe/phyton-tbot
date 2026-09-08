from aiogram import Bot, Router, F
from aiogram.filters import Command

from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from forms.user import Form
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

router = Router()


def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Open site", url="https://www.lvivyoga.club/")],
            [InlineKeyboardButton(text="Help", callback_data="info")],
        ]
    )

    return keyboard

def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="About")],
            [KeyboardButton(text="Help"), KeyboardButton(text="Start")],
        ],
        resize_keyboard=True,
    )

    return keyboard

@router.callback_query(lambda query: query.data == "info")
async def info(callback):
    await callback.message.answer('Here is more detailed info!')
    await callback.answer()

@router.message(Command("cancel"))
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Cancelled questionary")

@router.message(Command("start"))
@router.message(F.text.lover() == "cтарт")
async def start(message: Message, state: FSMContext):
    await message.answer("Lets fill your data first:")
    await state.set_state(Form.name)

@router.message(Form.name, F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Great! What is your age?")
    await state.set_state(Form.age)

@router.message(Form.age, F.text)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Please enter a number")
        return

    if int(message.text) < 6 or int(message.text) > 100:
        await message.answer("Please enter a valid age number")
        return

    await state.update_data(age=int(message.text))

    await message.answer("Great! What is your email?")
    await state.set_state(Form.email)

@router.message(Form.email, F.text)
async def process_email(message: Message, state: FSMContext):
    email = message.text
    if "@" not in email or "." not in email:
        await message.answer("Please enter a valid email address")
        return

    await state.update_data(email=message.text)
    data = await state.get_data()
    name = data["name"]
    age = data["age"]
    email = data["email"]

    await message.answer(f"Great! Here is your data! Name: {name}, Age: {age}, Email: {email}")
    await state.clear()

@router.message(F.photo)
async def process_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id

    await message.answer(f"Here is your photo! <code>{file_id}</code>", parse_mode="html")

    await message.answer_photo(file_id, caption="Here is your photo!")

@router.message(F.video)
async def process_video(message: Message):
    video = message.video
    file_id = video.file_id
    duration = video.duration

    await message.answer(f"Here is your video! Duration of video: <code>{duration}</code>", parse_mode="html")

    await message.answer_video(file_id, caption="Here is your video!")

@router.message(F.document)
async def process_document(message: Message, bot: Bot):
    document = message.document
    file_id = document.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path

    local_path = f'downloads/{document.file_name}'

    await bot.download_file(file_path=file_path, destination=local_path)

    await message.answer(f"File {document.file_name} has been downloaded")

@router.message(Command("file"))
async def send_file(message: Message):
    file = FSInputFile('files/example.txt')

    await message.answer_document(file)


@router.message(Command("help"))
async def start(message: Message):
    await message.answer("Available commands: \n /start - Start bot \n /help - Show this message \n /about - About me")

@router.message(Command("about"))
async def start(message: Message):
    await message.answer(f"Hi, {message.from_user.first_name}!\n ", reply_markup=get_main_inline_keyboard())

@router.message()
async def start(message: Message):
    await message.answer("Use commands from the list", reply_markup=get_main_reply_keyboard())