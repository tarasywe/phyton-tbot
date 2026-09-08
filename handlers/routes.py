from aiogram import Bot, Router, F
from aiogram.filters import Command

from aiogram.types import (
    Message,
    FSInputFile, User
)

import aiosqlite

DB_NAME = "database.db"

router = Router()

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
                     id INTEGER PRIMARY KEY,
                     full_name TEXT,
                     age INTEGER
                     )
        """)
        await db.commit()

async def add_user(full_name: str, age: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO users (full_name, age) VALUES (?, ?)", (full_name, age))
        await db.commit()

async def get_users() -> User:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT full_name, age FROM users")
        result = await cursor.fetchall()
        return result

@router.message(Command("start"))
async def start(message: Message):
    await init_db()
    await message.answer("Write command /reg AGE", parse_mode="HTML")

@router.message(Command("reg"))
async def start(message: Message):
    parts = message.text.strip().split()

    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("incorrect format of age")
        return

    await add_user(message.from_user.full_name, int(parts[1]))

    await message.answer("You have been registered!", parse_mode="HTML")


@router.message(Command("users"))
async def users(message: Message):
    users_list = await get_users()

    if not users_list:
        await message.answer("No users registered")
        return

    text = "all users:"
    for full_name, age in users_list:
        text += f"\nName: {full_name}: age: {age}"

    await message.answer(text, parse_mode="HTML")

