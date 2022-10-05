from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.database.get import result_info_team
from bot.database.post import add_user
from bot.reference_info import teams
from config import TELEGRAM_TOKEN
from bot.keyboards import *

leagues = [league.name for league in leagues]


class FSMAdmin(StatesGroup):
    league_state = State()
    team_h = State()
    team_g = State()
    condition = State()


storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    add_user(message.from_user.id)
    # await message.answer(f"Ваш ID: {message.from_user.id}")
    await message.answer('<b>Добро пожаловать!</b>\n' + '\n' + '<b>ЛИГУ --> КОМАНДЫ --> РЕЗУЛЬТАТ.</b>\n',
                         reply_markup=keyboard_1)


@dp.message_handler(Text, state=None)
async def cm_start(message: types.Message, state: FSMContext):
    await FSMAdmin.league_state.set()
    if message.text not in leagues:
        await message.answer("Выберите лигу из списка")
        await state.finish()
    else:
        async with state.proxy() as data:
            data['league_state'] = message.text
        await FSMAdmin.next()
        await message.answer('1.Выберите команду, которая играет дома:', reply_markup=get_keywords(message.text))


@dp.message_handler(Text(equals='Отменить ❌', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Выберите лигу из списка", reply_markup=keyboard_1)


# Ловим ответ от пользователя и пишем в словарь
@dp.message_handler(state=FSMAdmin.team_h)
async def load_team_1(message: types.Message, state: FSMContext):
    if message.text not in teams:
        await message.answer("Используйте кнопки")
    else:
        async with state.proxy() as data:
            data['team_h'] = message.text
        await FSMAdmin.next()
        await message.answer("2.Выберите команду, которая играет в гостях:",
                             reply_markup=get_keywords(data['league_state']))


# Ловим ответ
@dp.message_handler(state=FSMAdmin.team_g)
async def load_team_2(message: types.Message, state: FSMContext):
    if message.text not in teams:
        await message.answer("Используйте кнопки")
    else:
        async with state.proxy() as data:
            data['team_g'] = message.text
        await FSMAdmin.next()
        await message.answer("Если все верно, нажмите кнопку [Отправить]:", reply_markup=keyboard_2)


@dp.message_handler(Text, state=FSMAdmin.condition)
async def send_handler(message: types.Message, state: FSMContext):
    if message.text == "Отправить":
        async with state.proxy() as data:
            league_name = data["league_state"]
            team_home_name = data["team_h"]
            team_guest_name = data["team_g"]
            id_team_h: int = DICT_TEAM.get(DICT_LEAGUE.get(league_name)).get(team_home_name)
            id_team_g: int = DICT_TEAM.get(DICT_LEAGUE.get(league_name)).get(team_guest_name)
            if id_team_h == id_team_g:
                await message.answer("<b>Расчёт не произведен, так как вы выбрали одинаковые команды!</b>",
                                     reply_markup=keyboard_1)
            else:
                result_info = result_info_team(id_team_h, id_team_g)
                await message.answer(f"<b>Прогнозируемый тотал матча: {result_info.result.score.value}</b>\n" +
                                     "Ср. кол-во голов по статистике: \n" +
                                     f"{team_home_name} (дома) = <b>{result_info.result.score.team_home}</b>\n" +
                                     f"{team_guest_name} (в гостях) = <b>{result_info.result.score.team_guest}</b>\n" + "\n" +
                                     f"<b>Прогнозируемый тотал угловых: {result_info.result.corners.value}</b>\n" +
                                     "ИТ1: <b>{}</b>\n".format(result_info.result.corners.team_home) +
                                     "ИТ2: <b>{}</b>\n".format(result_info.result.corners.team_guest) + "\n" +
                                     "<b>Прогнозируемые тоталы: </b>\n" +
                                     "фолов = <b>{}</b>\n".format(result_info.result.fouls.value) +
                                     "офсайдов = <b>{}</b>\n".format(result_info.result.offsides.value) +
                                     "желтых карточек = <b>{}</b>\n".format(result_info.result.cards.value),
                                     reply_markup=keyboard_1)
            await state.finish()
    else:
        await message.answer("Используйте кнопки")
