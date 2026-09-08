import asyncio

from aiogram import Bot, Router
from aiogram.filters import Command

from aiogram.types import (
    Message,
)

router = Router()

subscribers = set()

async def notifier(bot: Bot):
    while True:
        if subscribers:
            for user_id in list(subscribers):
                try:
                    await bot.send_message(user_id, "Your default message!")
                except Exception:
                    pass
        await asyncio.sleep(10)

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Hello!\n"
        "I can help you with subscriptions\n"
        "Commands:\n"
        "/subscribe - subscribe for notifications\n"
        "/unsubscribe - unsubscribe for notifications\n"
        "/subscriptions - show subscriptions\n"
    )


@router.message(Command("subscribe"))
async def subscribe(message: Message):
    user_id = message.from_user.id

    subscribers.add(user_id)
    await message.answer("You are now subscribed!")

@router.message(Command("unsubscribe"))
async def unsubscribe(message: Message):
    user_id = message.from_user.id

    subscribers.discard(user_id)
    await message.answer("You are now unsubscribed!")

@router.message(Command("subscriptions"))
async def subscribers_command(message: Message):
    if not subscribers:
        await message.answer("No subscribers!")
        return

    text = "Subscribers:\n"
    for uid in list(subscribers):
        text += f"- {uid}\n"

    await message.answer(text)
