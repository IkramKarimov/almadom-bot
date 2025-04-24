from aiogram.fsm.state import State, StatesGroup

class AddApartment(StatesGroup):
    district = State()
    rooms = State()
    complex_name = State()
    year_built = State()
    price = State()
    area = State()
    floor_info = State()
    media = State()
    confirm = State()
    
    media = State()
    
    contact = State()