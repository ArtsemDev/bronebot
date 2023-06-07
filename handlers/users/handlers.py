from datetime import date, time, datetime

from aiogram import F
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InputFile
from aiogram.fsm.context import FSMContext
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from utils import generate_qrcode, generate_barcode
from utils.models import User, UserReservation
from .router import router
from keyboards.reply import main_panel_rkb
from keyboards.inline import DateCallbackData, GramDateInlineKeyboardMarkup, \
    GramTimeInlineKeyboardMarkup, TimeCallbackData, \
    ReservationCallbackData, reservation_panel_ikb, reservation_list_ikb
from settings import BASE_DIR
from states import RevisionStateGroup


@router.message(F.text.startswith('/start'))
async def start_command(message: Message):
    user = User(id=message.from_user.id)
    async with User.session() as session:
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            text = f'Привет {message.from_user.first_name}, Давно не виделись!'
        else:
            text = f'Добро пожаловать {message.from_user.first_name}! Я бот по бронированию столиков!'
        finally:
            await message.answer(
                text=text,
                reply_markup=main_panel_rkb
            )


@router.message(F.text == main_panel_rkb.keyboard[0][1].text)
async def menu_handler(message: Message):
    await message.delete()
    await message.answer_photo(
        photo='AgACAgIAAxkDAAOcZIDLvlNgBS4cTf7WK2WmEqbyBw0AAoLGMRtBHwABSLymwF7nMefyAQADAgADeQADLwQ',
        caption='MENU'
    )


@router.message(F.text == main_panel_rkb.keyboard[0][0].text)
async def reservation_handler(message: Message):
    await message.delete()
    await message.answer(
        text='Выберите действие!',
        reply_markup=reservation_panel_ikb
    )


@router.callback_query(ReservationCallbackData.filter(F.action == 'book'))
async def reservation_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RevisionStateGroup.count)
    await callback.message.edit_text(
        text='<b>Введите количество гостей!</b>'
    )


@router.message(RevisionStateGroup.count)
async def get_count_quests(message: Message, state: FSMContext):
    await message.delete()
    try:
        count_quests = int(message.text)
    except ValueError:
        await message.answer(
            text='Неверное количество!'
        )
    else:
        if count_quests > 0:
            await state.set_state(RevisionStateGroup.date)
            await state.update_data({'count': count_quests})
            await message.answer(
                text=f'<b>ВЫБЕРИТЕ ДАТУ!</b>',
                reply_markup=await GramDateInlineKeyboardMarkup.create()
            )
        else:
            await message.answer(
                text='Неверное количество!'
            )


@router.callback_query(DateCallbackData.filter(), RevisionStateGroup.date)
async def select_date(callback: CallbackQuery, callback_data: DateCallbackData, state: FSMContext):
    response = await GramDateInlineKeyboardMarkup.parse(callback_data)
    if isinstance(response, date):
        await state.set_state(RevisionStateGroup.time)
        await state.update_data({'date': response})
        await callback.message.edit_text(
            text='<b>ВЫБЕРИТЕ ВРЕМЯ!</b>',
            reply_markup=await GramTimeInlineKeyboardMarkup.create()
        )
    else:
        await callback.message.edit_reply_markup(
            reply_markup=response
        )


@router.callback_query(TimeCallbackData.filter(), RevisionStateGroup.time)
async def select_time(callback: CallbackQuery, callback_data: TimeCallbackData, state: FSMContext):
    response = await GramTimeInlineKeyboardMarkup.parse(callback_data)
    if isinstance(response, time):
        state_data = await state.get_data()
        await state.clear()
        state_data['time'] = response
        reservation_datetime = datetime(
            day=state_data.get('date').day,
            month=state_data.get('date').month,
            year=state_data.get('date').year,
            hour=state_data.get('time').hour,
            minute=state_data.get('time').minute,
        )
        async with UserReservation.session() as session:
            reservation = UserReservation(
                user_id=callback.from_user.id,
                date_reservation=reservation_datetime,
                number_of_quests=state_data.get('count')
            )
            session.add(reservation)
            try:
                await session.commit()
            except IntegrityError:
                await callback.message.edit_text(
                    text='Произошла ошибка! Повторите попытку или обратитесь в поддержку!'
                )
            else:
                keyboard = await reservation_list_ikb(user_id=callback.from_user.id)
                keyboard.inline_keyboard.append(reservation_panel_ikb.inline_keyboard[0])
                await callback.message.edit_text(
                    text=f'<i>Вы забронировали столик на </i><b>{state_data.get("count")}</b><i> человек</i>\n'
                         f'<i>Дата:</i> <b>{state_data.get("date").strftime("%d %m %Y")}</b>\n'
                         f'<i>Время:</i> <b>{state_data.get("time").strftime("%H:%M")}</b>',
                    reply_markup=keyboard
                )
    else:
        await callback.message.edit_reply_markup(
            reply_markup=response
        )


@router.callback_query(ReservationCallbackData.filter(F.action == 'mybook'))
async def user_reservation(callback: CallbackQuery):
    response = await reservation_list_ikb(user_id=callback.from_user.id)
    response.inline_keyboard.append(reservation_panel_ikb.inline_keyboard[0])
    if response:
        await callback.message.edit_text(
            text='Ваши брони! Можете удалить ненужную!',
            reply_markup=response
        )
    else:
        await callback.message.edit_text(
            text='Брони нет!',
            reply_markup=reservation_panel_ikb
        )


@router.callback_query(ReservationCallbackData.filter(F.action == 'delete'))
async def delete_reservation(callback: CallbackQuery, callback_data: ReservationCallbackData):
    async with UserReservation.session() as session:
        await session.execute(
            delete(UserReservation)
            .filter_by(id=callback_data.reservation_id)
        )
        await session.commit()
    keyboard = await reservation_list_ikb(user_id=callback.from_user.id)
    await callback.answer(
        text='БРОНЬ БЫЛА УДАЛЕНА!'
    )
    if keyboard:
        keyboard.inline_keyboard.append(reservation_panel_ikb.inline_keyboard[0])
        text = 'Ваши брони! Можете удалить ненужную!'
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[reservation_panel_ikb.inline_keyboard[0]]
        )
        text = 'Броней больше нет!'
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@router.message(F.text == main_panel_rkb.keyboard[1][0].text)
async def balance(message: Message):
    await message.delete()
    qr = generate_barcode(payload=message.from_user.id)
    async with User.session() as session:
        user = await session.get(User, message.from_user.id)
    await message.answer_photo(
        photo=BufferedInputFile(qr, filename='qr.png'),
        caption=f'<i>Ваш баланс бонусных баллов:</i> <b>{user.balance}</b>'
    )
