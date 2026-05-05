import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice, PreCheckoutQuery, Message
)

# ==============================
# НАСТРОЙКИ — ЗАПОЛНИ СВОИМИ ДАННЫМИ
# ==============================
BOT_TOKEN = "ВСТАВЬ_ТОКЕН_СЮДА"  # Токен от @BotFather
PACK_FILE_ID = "ВСТАВЬ_FILE_ID_ПАКА_СЮДА"  # File ID архива с паком (читай инструкцию ниже)
PACK_PRICE_STARS = 50  # Цена в Telegram Stars (50 Stars ≈ ~150 руб)
ADMIN_ID = 123456789  # Твой Telegram ID (узнай у @userinfobot)
# ==============================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главное меню
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 Купить пак — 50 Stars", callback_data="buy")],
        [InlineKeyboardButton(text="📦 Что входит в пак?", callback_data="info")],
    ])

# /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👾 Привет! Я бот <b>Pro Optimize</b>\n\n"
        "🚀 Продаю пак для максимальной оптимизации твоего ПК:\n"
        "• Твики реестра\n"
        "• .bat скрипты для чистки системы\n"
        "• Отключение лишних служб\n"
        "• Настройки для буста FPS\n\n"
        "Выбери действие 👇",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# Что входит в пак
@dp.callback_query(F.data == "info")
async def info(callback: types.CallbackQuery):
    await callback.message.answer(
        "📦 <b>Что входит в пак Pro Optimize:</b>\n\n"
        "✅ Твики реестра Windows 10/11\n"
        "✅ .bat скрипты — чистка системы одной кнопкой\n"
        "✅ Отключение фоновых служб и телеметрии\n"
        "✅ Настройки мыши, сети и графики для игр\n"
        "✅ PDF инструкция по применению\n\n"
        "💰 Цена: <b>50 Telegram Stars</b> (~150 руб)\n\n"
        "После оплаты — файл придёт автоматически! 🎉",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💸 Купить!", callback_data="buy")]
        ])
    )
    await callback.answer()

# Кнопка купить — отправляем инвойс
@dp.callback_query(F.data == "buy")
async def buy(callback: types.CallbackQuery):
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="Pro Optimize Pack",
        description="Пак твиков, скриптов и настроек для максимальной оптимизации ПК и буста FPS",
        payload="pro_optimize_pack",
        currency="XTR",  # XTR = Telegram Stars
        prices=[LabeledPrice(label="Pro Optimize Pack", amount=PACK_PRICE_STARS)],
        provider_token=""  # Для Stars оставить пустым
    )
    await callback.answer()

# Проверка перед оплатой
@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

# Успешная оплата — отправляем файл
@dp.message(F.successful_payment)
async def payment_done(message: Message):
    user = message.from_user
    stars = message.successful_payment.total_amount

    # Уведомление админу
    await bot.send_message(
        ADMIN_ID,
        f"✅ Новая оплата!\n"
        f"👤 {user.full_name} (@{user.username})\n"
        f"⭐ {stars} Stars"
    )

    # Отправляем пак покупателю
    await message.answer("✅ Оплата прошла! Отправляю пак...")

    if PACK_FILE_ID == "ВСТАВЬ_FILE_ID_ПАКА_СЮДА":
        # Если файл ещё не добавлен — отправляем заглушку
        await message.answer(
            "📦 Пак будет отправлен в ближайшее время!\n"
            "Если не получил в течение 5 минут — напиши @prooptimiz"
        )
    else:
        await bot.send_document(
            message.chat.id,
            document=PACK_FILE_ID,
            caption="🚀 <b>Pro Optimize Pack</b>\n\nЧитай инструкцию внутри архива!\nЕсли есть вопросы — @prooptimiz",
            parse_mode="HTML"
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
