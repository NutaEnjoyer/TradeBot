import datetime
import time
from PIL import Image, ImageDraw, ImageFont
import pytz
from models import *
import data.config as config

def add_text_to_image(image_path, text, output_path):
    # Load the image
    image = Image.open(image_path)

    # Initialize the font and text color
    font = ImageFont.truetype("arial.ttf", 56)
    text_color = (255, 255, 255)  # RGB value for white

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Determine the position to add the text
    # text_width, text_height = draw.textlength(text, font)
    x = (image.width - 150) // 2
    y = (image.height - 20) // 2.5

    # Add the text to the image
    draw.text((x, y), text, font=font, fill=text_color)

    # Save the modified image
    image.save(output_path)

def make_profit_image(image_path, profits, output_path):
    # Load the image
    profit, full_profit = profits
    image = Image.open(image_path)

    # Initialize the font and text color
    font = ImageFont.truetype("arial.ttf", 56)
    text_color = (255, 255, 255)  # RGB value for white

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Determine the position to add the text
    # text_width, text_height = draw.textlength(text, font)
    x = (image.width - 150) // 2
    y = (image.height - 20) // 2.5

    # Add the text to the image
    draw.text((x, y), profit, font=font, fill=text_color)
    # draw.text((x, y), profit, font=font, fill=text_color)

    # Save the modified image
    image.save(output_path)

def check_amount(text, user):
    if not text.isdigit():
        return
    cfg = get_my_config(user.user_id)

    price = int(text)
    if price < cfg.min_deposite or price > 10_000_000:
        return
    return price 

def check_future_amount(text, user):
    if not text.isdigit():
        return

    currency = Currency.get(id=user.currency)
    min_bet = round(config.min_bet / currency.exchange_rate)

    price = int(text)

    if price > user.balance:
        return 
    
    if price < min_bet:
        return
    return price * currency.exchange_rate

def gif(price_list, coin_name, id):
    import matplotlib
    import matplotlib.pyplot as plt

    interval = len(price_list) // 15

    matplotlib.use('agg')

    selected_numbers = []

    for i in range(0, len(price_list), interval):
        selected_numbers.append(price_list[i])
    price_list = selected_numbers

    plt.plot(price_list)
    plt.title(f'График цен на {coin_name}')
    plt.savefig(f'{id}.png')

def get_my_config(user_id):
    self_config = SelfConfig.get_or_none(user_id=user_id)
    if self_config: return self_config
    family = Family.get_or_none(baby_id=user_id)
    if family:
        worker_config = WorkerConfig.get(worker_id=family.user_id)
        return worker_config
    
    cfg = WorkerConfig.get(worker_id=config.LOGGER_CHAT)
    return cfg


def get_my_config_id(user_id):
    family = Family.get_or_none(baby_id=user_id)
    if family:
        worker_config = WorkerConfig.get(worker_id=family.user_id)
        return worker_config.worker_id
    
    cfg = WorkerConfig.get(worker_id=config.LOGGER_CHAT)
    return cfg.worker_id

def withdraw_photo(req, price, name):
    price = str(price) + ' P'
    req = str(req)
    utc_now = datetime.datetime.now(pytz.utc)
    moscow_tz = pytz.timezone("Europe/Moscow")
    moscow_now = utc_now.astimezone(moscow_tz)
    formatted_date = moscow_now.strftime("%Y-%m-%d %H:%M:%S")

    image = Image.open('images/BBB.png')

    # Initialize the font and text color
    font = ImageFont.truetype("arial.ttf", 36)
    text_color = (0, 0, 0)  # RGB value for white

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Determine the position to add the text
    # text_width, text_height = draw.textlength(text, font)
    x = (image.width - 150) // 2
    y = (image.height - 20) // 2.5

    draw.text(((image.width - 150) // 4.3, (image.height - 20) // 2.8), req, font=font, fill=text_color)
    draw.text(((image.width - 150) // 6, (image.height - 20) // 2.257), price, font=font, fill=text_color)
    draw.text(((image.width - 150) // 7.2, (image.height - 20) // 1.88), formatted_date, font=font, fill=text_color)
    draw.text(((image.width - 150) // 7.25, (image.height - 20) // 1.62), name, font=font, fill=text_color)

    path = f'images/{time.time()}.png'
    image.save(path)

    return path
    
    
if __name__ == '__main__':
    withdraw_photo(req='1234123412341234', price=1000, name='Max')
    