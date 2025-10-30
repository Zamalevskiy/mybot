import os
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

router = Router()

import os

photo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "me.JPG")

# Открываем файл и отправляем
with open(photo_path, "rb") as photo:
    await message.answer_photo(photo)



@router.callback_query(F.data == "chapter_02")
async def chapter_02_handler(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Вернуться и получить помощь",
        callback_data="chapter_01"  # теперь корректно ведёт на обработчик chapter_01
    )
    builder.adjust(1)

    text = (
        "<b>Привет! Я - Алексей Замалевский, и я знаю, каково это - когда в жизни бардак и всё валится из рук…</b>\n\n"
        "Я коуч, психолог и уже 5 лет занимаюсь кризисным консультированием. "
        "За это время помог сотням людей справиться с тревогой, усталостью и ощущением, что жизни больше нет.\n\n"
        "Но если честно, у меня самого было не легче. "
        "В 2019 году случился тяжёлый развод - всё, что казалось привычным и надёжным, разрушилось. "
        "Появились проблемы на работе, со здоровьем, и внутри будто пустота. "
        "Я помню это ощущение: когда кажется, что выхода нет и никто тебе не поможет.\n\n"
        "Через свой опыт я понял одну вещь: <b>любой кризис можно пройти, если есть поддержка и конкретные инструменты</b>, "
        "которые помогают вернуть ясность и внутреннюю опору. "
        "Именно в этом я помогаю тем, кто ко мне обращается. Чтобы они чувствовали - <b>они не одни, и решения есть</b>.\n\n"
        "Вернись и выбери, что тебе ближе сейчас - я помогу!"
    )

    # Отправка фото с текстом
    if os.path.exists(PHOTO_PATH):
        photo = FSInputFile(PHOTO_PATH)
        await callback.message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=builder.as_markup()
        )
    else:
        # Если фото не найдено
        await callback.message.answer(
            text + "\n\nФото не найдено.",
            reply_markup=builder.as_markup()
        )

    await callback.answer()
