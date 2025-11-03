from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from analytics import log_event

router = Router()


@router.callback_query(F.data == "chapter_04")
async def chapter_04_handler(callback: types.CallbackQuery):
    # Логирование нажатия кнопки
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="button_click",
        action_name="chapter_04",
        additional_data=""
    )
    
    builder = InlineKeyboardBuilder()
    builder.button(
        text="☀️Вернуть радость себе",
        callback_data="chapter_08"
    )

    text = (
        "<b>Когда всё вроде правильно - работа, семья, порядок… а внутри тишина.</b>\n\n"
        "Ты не одна.\n"
        "Это не каприз и не «неблагодарность». Просто долго жила на автопилоте - выполняла, справлялась, держала всех и всё.\n"
        "А сейчас ресурс закончился, и тело говорит: «Стоп. Пора вспомнить про себя».\n\n"
        "«Наталья пришла с чувством, что “жизнь без вкуса”: всё делается по инерции.\n"
        "Мы разобрали, где она теряет энергию - оказалось, почти весь день уходит на “надо”.\n"
        "Постепенно добавили короткие ритуалы радости: утренний кофе на балконе, пятиминутное дыхание перед работой, прогулку без телефона.\n"
        "Через неделю она написала: “Я впервые за долгое время просто улыбнулась - без причины”.»\n\n"
        "<b>Я собрал короткий гайд «Как вернуть радость и вкус к жизни, когда внутри пусто».\n"
        "В нём простые шаги, которые помогают почувствовать себя живой, даже если кажется, что ничего не радует.\n"
        "Без “мотивации” и теорий - только то, что реально работает, когда нет сил.</b>"
    )

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()
