from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from analytics import log_event

router = Router()


@router.callback_query(F.data == "chapter_05")
async def chapter_05_handler(callback: types.CallbackQuery):
    # Логирование нажатия кнопки
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="button_click",
        action_name="chapter_05",
        additional_data=""
    )
    
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✨Обрести уверенность и путь",
        callback_data="chapter_09"
    )

    text = (
        "<b>Когда всё кажется бессмысленным и впереди пустота — это не конец, а начало новой главы.</b>\n\n"
        "Ты не сломалась - просто закончилась старая роль, а новая ещё не родилась.\n"
        "Это больно, потому что всё, что раньше держало, вдруг перестало работать: дети выросли, отношения изменились, работа не вдохновляет.\n"
        "Но это не провал - это переход. И в переходе важно не “собраться”, а понять, кто ты теперь, и чего хочешь на самом деле.\n\n"
        "«Наталья пришла с чувством, что жизнь кончилась: развод, тишина в квартире, пустые вечера.\n"
        "Она говорила: “Я не знаю, кем быть, если не мама и не жена.”\n"
        "Мы начали с простых шагов - восстановили базовую опору, вернули маленькие радости, вспомнили, что раньше зажигало.\n"
        "Через месяц она сказала: “Я снова просыпаюсь с желанием что-то делать. Я не потерялась - просто началась другая я.”»\n\n"
        "<b>Я подготовил короткий гайд “Как вернуть себе радость, когда внутри пусто” - простые шаги, которые помогают ожить, когда кажется, что всё потеряно.\n"
        "Там нет сложной психологии - только живые, реальные способы вернуть вкус к жизни и почувствовать, что всё ещё можно.</b>"
    )

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()
