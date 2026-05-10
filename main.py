import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# ТОКЕН ТВОЕГО БОТА (получи у @BotFather)
TOKEN = "8789099029:AAF5EIxPOE5UBTYJJqQepF4h3Pon00xOFBE"

# ID твоего Telegram аккаунта (можно узнать у @userinfobot)
ALLOWED_USER_ID = 1713842880

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Функция создания главной клавиатуры с кнопками
def get_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="🔻 Выключить через 10 сек", callback_data="shutdown_delayed"),
        InlineKeyboardButton(text="⛔ ВЫКЛЮЧИТЬ СЕЙЧАС", callback_data="shutdown_now")
    )
    builder.row(
        InlineKeyboardButton(text="❌ Отменить выключение", callback_data="cancel_shutdown"),
        InlineKeyboardButton(text="❓ Помощь", callback_data="help")
    )

    return builder.as_markup()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    if message.from_user.id != ALLOWED_USER_ID:
        await message.answer("❌ У тебя нет прав доступа к этому боту.")
        return

    await message.answer(
        "✅ *Бот активирован!*\n\n"
        "Используй кнопки ниже для управления ноутбуком:\n\n"
        "🔻 *Выключение через 10 сек* — безопасное выключение\n"
        "⛔ *Выключение сейчас* — мгновенное выключение\n"
        "❌ *Отменить выключение* — только для Windows\n\n"
        "⚠️ *Внимание:* После выключения бот перестанет отвечать!",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )


@dp.callback_query(lambda c: c.data == "help")
async def help_callback(callback: types.CallbackQuery):
    if callback.from_user.id != ALLOWED_USER_ID:
        await callback.answer("Нет доступа!", show_alert=True)
        return

    await callback.message.edit_text(
        "🖥️ *Управление ноутбуком через кнопки*\n\n"
        "🔻 *Выключение через 10 сек* — ноутбук выключится через 10 секунд. Можно отменить.\n\n"
        "⛔ *Выключение сейчас* — мгновенное выключение. Отменить НЕЛЬЗЯ!\n\n"
        "❌ *Отмена выключения* — работает только на Windows. Отменяет запланированное выключение.\n\n"
        "⚠️ После выключения бот перестанет отвечать до перезапуска системы.\n\n"
        "🔄 *Чтобы вернуться в меню* — нажми /start",
        parse_mode="Markdown"
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "shutdown_delayed")
async def shutdown_delayed_callback(callback: types.CallbackQuery):
    if callback.from_user.id != ALLOWED_USER_ID:
        await callback.answer("Нет доступа!", show_alert=True)
        return

    await callback.message.edit_text(
        "⚠️ *Ноутбук выключится через 10 секунд!*\n\n"
        "Нажми ❌ *Отменить выключение* если передумал (только Windows).",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

    if sys.platform == "win32":
        os.system("shutdown /s /t 10")
    elif sys.platform == "linux" or sys.platform == "darwin":
        os.system("shutdown -h +0.1")
    else:
        await callback.message.answer("❌ Неподдерживаемая ОС.")

    await callback.answer("✅ Выключение запланировано!")


@dp.callback_query(lambda c: c.data == "shutdown_now")
async def shutdown_now_callback(callback: types.CallbackQuery):
    if callback.from_user.id != ALLOWED_USER_ID:
        await callback.answer("Нет доступа!", show_alert=True)
        return

    await callback.message.edit_text(
        "⚠️⚠️⚠️ *НОУТБУК ВЫКЛЮЧАЕТСЯ СЕЙЧАС!* ⚠️⚠️⚠️\n\n"
        "_До связи после перезагрузки..._",
        parse_mode="Markdown"
    )
    await callback.answer("ВНИМАНИЕ! Выключение!")

    if sys.platform == "win32":
        os.system("shutdown /s /t 0")
    elif sys.platform == "linux" or sys.platform == "darwin":
        os.system("shutdown -h now")
    else:
        await callback.message.answer("❌ Неподдерживаемая ОС.")


@dp.callback_query(lambda c: c.data == "cancel_shutdown")
async def cancel_shutdown_callback(callback: types.CallbackQuery):
    if callback.from_user.id != ALLOWED_USER_ID:
        await callback.answer("Нет доступа!", show_alert=True)
        return

    if sys.platform == "win32":
        os.system("shutdown /a")
        await callback.message.edit_text(
            "✅ *Выключение отменено!*\n\n"
            "Ноутбук продолжит работу.",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        await callback.answer("Отмена выполнена!")
    else:
        await callback.answer("❌ Отмена выключения доступна только в Windows!", show_alert=True)


# Обработка обычных команд как альтернатива (не обязательно, но для удобства)
@dp.message(Command("shutdown"))
async def shutdown_delayed_command(message: types.Message):
    if message.from_user.id != ALLOWED_USER_ID:
        return

    await message.answer("⚠️ Выключение через 10 секунд!", reply_markup=get_main_keyboard())

    if sys.platform == "win32":
        os.system("shutdown /s /t 10")
    elif sys.platform == "linux" or sys.platform == "darwin":
        os.system("shutdown -h +0.1")


@dp.message(Command("shutdown_now"))
async def shutdown_now_command(message: types.Message):
    if message.from_user.id != ALLOWED_USER_ID:
        return

    await message.answer("⚠️⚠️⚠️ НОУТБУК ВЫКЛЮЧАЕТСЯ СЕЙЧАС!")

    if sys.platform == "win32":
        os.system("shutdown /s /t 0")
    elif sys.platform == "linux" or sys.platform == "darwin":
        os.system("shutdown -h now")


@dp.message(Command("cancel"))
async def cancel_command(message: types.Message):
    if message.from_user.id != ALLOWED_USER_ID:
        return

    if sys.platform == "win32":
        os.system("shutdown /a")
        await message.answer("✅ Выключение отменено!", reply_markup=get_main_keyboard())


async def main():
    print("🚀 Бот запущен...")
    print("✅ Используй кнопки в Telegram для управления ноутбуком")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())