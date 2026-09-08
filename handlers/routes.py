from aiogram import Bot, Router, F
from aiogram.filters import Command

from aiogram.types import (
    Message,
    FSInputFile
)

import aiohttp

router = Router()

async def get_product(product_id):
    url = f"https://fakestoreapi.com/products/{product_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 404:
                return None

            data = await resp.json()
            return data


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("set command /product with ID: <b>/product ID</b>", parse_mode="HTML")

@router.message(Command("product"))
async def get_product_cmd(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 2:
        await message.answer("From format of request, use /product 1")
        return

    product_id = parts[1]
    if not product_id.isdigit():
        await message.answer("From format of request, use /product and number")
        return

    await message.answer(f"All fine, looking for {product_id}")

    try:
        product = await get_product(int(product_id))
    except Exception:
        await message.answer("Servers return error")
        return

    if product is None:
        await message.answer("Product not found")
        return

    title = product.get("title", 'Untitled')
    price = product.get("price", '0.0')
    description = product.get("description", 'No description')
    category = product.get("category", 'No category')
    # image = product.get("image")

    text = (
        f"<b>{title}</b>\n\n"
        f"Category: {category}\n\n"
        f"Price: {price}\n\n"
        f"Description: {description}\n\n"
    )

    photo = FSInputFile("image.jpeg")


    # if image:
    await message.answer_photo(photo=photo, caption=text, apparse_mode="HTML")
    # else:
        # await message.answer(text, parse_mode="HTML")