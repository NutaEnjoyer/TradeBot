import matplotlib.pyplot as plt
from PIL import Image, ImageFile

# Создание списка данных для каждого кадра
data_frames = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8]]

# Создание списка цветов для каждого столбца
colors = ['red', 'green', 'red', 'green']

# Создание списка изображений для сохранения каждого кадра
images = []
ImageFile.LOAD_TRUNCATED_IMAGES = True

price_data = [100, 105, 98, 102, 110, 115, 112, 120, 125]

# Создание графиков для каждого кадра
for frame_data, color in zip(data_frames, colors):

# Пример данных для графика цены на фондовом рынке

    fig, ax = plt.subplots()
    ax.plot(range(len(price_data)), price_data, color='blue')
    ax.set_xlabel('Perioд')
    ax.set_ylabel('Цена')
    ax.set_title('График цены на фондовом рынке')

    # Сохранение графика как изображения в память
    plt.savefig('stock_price_graph.png')
    image = Image.open('stock_price_graph.png')
    images.append(image)

# Сохранение изображений в виде анимированной GIF
images[0].save('simulation.gif', save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)