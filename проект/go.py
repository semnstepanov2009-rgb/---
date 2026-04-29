import pyvista as pv
import os
import numpy as np
import colorsys

print("=" * 60)
print("    3D МОДЕЛЬ - ВЫБОР ДЕТАЛЕЙ С ПОДПИСЯМИ И ОПИСАНИЕМ")
print("=" * 60)

# -------------------------------
# 1. Поиск файла модели
# -------------------------------
model_file = None
for file in os.listdir('.'):
    if file.lower().endswith(('.glb', '.gltf', '.obj', '.stl', '.ply')):
        model_file = file
        break

if model_file is None:
    print("\n❌ 3D модель не найдена!")
    exit()

print(f"\n✅ Найдена модель: {model_file}")
print(f"📂  Загружаем...")

# -------------------------------
# 2. Загрузка модели и сбор деталей
# -------------------------------
data = pv.read(model_file)

all_parts = []

def collect(obj):
    if isinstance(obj, pv.MultiBlock):
        for block in obj:
            if block:
                collect(block)
    else:
        if hasattr(obj, 'n_points') and obj.n_points > 0:
            all_parts.append(obj)

collect(data)
total_parts = len(all_parts)
print(f"✅ Найдено деталей: {total_parts}")

if total_parts == 0:
    print("❌ Нет деталей для отображения!")
    exit()

# -------------------------------
# 3. Имена деталей (индекс → название)
# -------------------------------
part_names = {
    0: "адаптер",
    1: "колёсная пара",
    2: "адаптер",
    3: "колёсная пара",
    4: "адаптер",
    5: "адаптер",
    6: "рессорный комплект",
    7: "букса",
    8: "букса",
    9: "букса",
    10: "букса",
    11: "надрессорная балка",
    12: "тормозная система",
    13: "боковая рама",
    14: "боковая рама",
}

# Дополняем, если деталей больше
for i in range(total_parts):
    if i not in part_names:
        part_names[i] = f"деталь_{i+1}"

# -------------------------------
# 4. Описания деталей (ключ – название из part_names)
# -------------------------------
part_descriptions = {
    "адаптер": {
        "description": "Переходной элемент между узлами",
        "functions": "• Соединение разнородных деталей\n• Компенсация зазоров\n• Передача нагрузки",
        "material": "Сталь 40Х, ГОСТ 4543-2016",
        "weight": "15–25 кг",
        "wear": "Средний износ, проверять раз в полгода"
    },
    "колёсная пара": {
        "description": "Основной ходовой элемент вагона",
        "functions": "• Обеспечивает движение по рельсам\n• Передаёт нагрузку на путь\n• Воспринимает динамические удары",
        "material": "Сталь марки 2, ГОСТ 10791-2011",
        "weight": "1200–1500 кг",
        "wear": "Контролировать прокат и толщину обода"
    },
    "рессорный комплект": {
        "description": "Система амортизации тележки",
        "functions": "• Гашение вертикальных колебаний\n• Смягчение ударов\n• Распределение нагрузки",
        "material": "Сталь 60С2А, ГОСТ 14959-2016",
        "weight": "80–120 кг",
        "wear": "Проверять просадку и целостность листов"
    },
    "букса": {
        "description": "Узел крепления подшипников колёсной пары",
        "functions": "• Фиксация оси\n• Смазка подшипников\n• Защита от загрязнений",
        "material": "Сталь 25Л, ГОСТ 977-88",
        "weight": "40–60 кг",
        "wear": "Контролировать нагрев и уровень смазки"
    },
    "надрессорная балка": {
        "description": "Несущая поперечная балка тележки",
        "functions": "• Связь боковых рам\n• Опора для кузова\n• Размещение пятника и скользунов",
        "material": "Сталь 20ГЛ, ГОСТ 977-88",
        "weight": "350–450 кг",
        "wear": "Осмотр на трещины, дефектоскопия"
    },
    "тормозная система": {
        "description": "Рычажно-тормозная передача",
        "functions": "• Снижение скорости\n• Экстренная остановка\n• Удержание на уклоне",
        "material": "Чугун СЧ20, ГОСТ 1412-85",
        "weight": "150–200 кг",
        "wear": "Проверять толщину колодок, состояние тяг"
    },
    "боковая рама": {
        "description": "Силовой каркас тележки",
        "functions": "• Опора для рессор\n• Передача тяговых усилий\n• Фиксация букс",
        "material": "Сталь 20ГФЛ, ГОСТ 977-88",
        "weight": "400–500 кг",
        "wear": "Дефектоскопия, контроль геометрии"
    }
}

# Описание по умолчанию
default_description = {
    "description": "Деталь вагона",
    "functions": "• Входит в состав ходовой части",
    "material": "Сталь конструкционная",
    "weight": "Зависит от типоразмера",
    "wear": "Согласно регламенту"
}

# -------------------------------
# 5. Подготовка Plotter'а
# -------------------------------
plotter = pv.Plotter(window_size=[1400, 900])
plotter.set_background('white')

# Проверяем наличие шрифта Arial
font_path = "C:/Windows/Fonts/arial.ttf"
if not os.path.exists(font_path):
    font_path = None  # PyVista будет использовать стандартный шрифт

# Генерация цветов для деталей
colors = []
for i in range(total_parts):
    if total_parts == 1:
        colors.append((0.7, 0.7, 0.7))
    else:
        hue = i / total_parts
        rgb = colorsys.hsv_to_rgb(hue, 0.6, 0.8)
        colors.append(rgb)

# -------------------------------
# 6. Добавление деталей и текстовых меток
# -------------------------------
actors_dict = {}

for i, part in enumerate(all_parts):
    name = part_names.get(i, f'Деталь_{i+1}')
    print(f"   Добавлена: {name}")

    # Сама деталь
    actor = plotter.add_mesh(part,
                             color=colors[i],
                             name=f"part_{i}",
                             pickable=True)
    actors_dict[i] = actor

    # Центр детали для размещения метки
    center = part.center if hasattr(part, 'center') else np.mean(part.points, axis=0)

    # Текстовая метка возле детали
    plotter.add_point_labels(points=[center],
                             labels=[name],
                             font_size=12,
                             text_color='black',
                             fill_shape=False,
                             point_size=0.1,
                             name=f"label_{i}",
                             font_file=font_path)

# -------------------------------
# 7. Информационная панель (верхний левый угол)
# -------------------------------
info_panel = plotter.add_text("ℹ️  ИНФОРМАЦИЯ\nВыберите деталь",
                              position='upper_left',
                              font_size=11,
                              color='black',
                              name="info_panel",
                              font_file=font_path)



# -------------------------------
# 9. Подсказка сверху
# -------------------------------
plotter.add_text(
    "Shift+ЛКМ — выбрать | ЛКМ+drag — вращать | ПКМ+drag — двигать | Колёсико — масштаб",
    position='upper_edge',
    font_size=9,
    color='gray',
    name="help_text",
    font_file=font_path)

# -------------------------------
# 10. Логика выбора
# -------------------------------
state = {"selected_index": None}


def reset_highlight(index):
    if index is not None and index in actors_dict:
        actor = actors_dict[index]
        actor.GetProperty().SetEdgeVisibility(False)
        actor.GetProperty().SetColor(colors[index])


def apply_highlight(index):
    if index is not None and index in actors_dict:
        actor = actors_dict[index]
        actor.GetProperty().SetColor(0.0, 1.0, 0.0)
        actor.GetProperty().SetEdgeVisibility(True)
        actor.GetProperty().SetEdgeColor(1.0, 0.0, 0.0)
        actor.GetProperty().SetLineWidth(3.0)


def format_info_text(part_name):
    """Формирует простой текст для информационной панели."""
    info = part_descriptions.get(part_name, default_description)
    lines = [
        f"ДЕТАЛЬ: {part_name}",
        f"",
        f"Назначение: {info['description']}",
        f"",
        f"Функции:",
        f"{info['functions']}",
        f"",
        f"Материал: {info['material']}",
        f"Масса: {info['weight']}",
        f"Износ: {info['wear']}"
    ]
    return "\n".join(lines)


def on_pick(picked):
    global current_text, info_panel

    if picked is None:
        return

    # Определяем индекс выбранной детали
    selected_index = None
    try:
        picked_addr = picked.GetAddressAsString("")
    except:
        picked_addr = ""

    for i, part in enumerate(all_parts):
        try:
            part_addr = part.GetAddressAsString("")
        except:
            part_addr = ""
        if picked_addr and part_addr and picked_addr == part_addr:
            selected_index = i
            break

    if selected_index is None:
        for i, part in enumerate(all_parts):
            if picked is part:
                selected_index = i
                break

    if selected_index is None:
        return

    # Снимаем подсветку с предыдущей детали
    prev = state["selected_index"]
    if prev is not None and prev != selected_index:
        reset_highlight(prev)

    # Подсвечиваем выбранную
    apply_highlight(selected_index)
    state["selected_index"] = selected_index

    # Название детали
    part_name = part_names.get(selected_index, f"деталь_{selected_index+1}")

    # ---------- Обновляем информационную панель ----------
    plotter.remove_actor(info_panel)
    info_display = format_info_text(part_name)
    info_panel = plotter.add_text(info_display,
                                  position='upper_left',
                                  font_size=11,
                                  color='black',
                                  name="info_panel",
                                  font_file=font_path)

    # ---------- Обновляем нижний текст ----------
    plotter.remove_actor(current_text)
    current_text = plotter.add_text(f"ВЫБРАНА ДЕТАЛЬ: {part_name}",
                                    position='lower_edge',
                                    font_size=24,
                                    color='red',
                                    name="selection_display",
                                    font_file=font_path)

    plotter.render()

    # Вывод в консоль
    print(f"\n✅ ВЫБРАНА ДЕТАЛЬ: {part_name}")
    info = part_descriptions.get(part_name, default_description)
    print(f"   📝  {info['description']}")
    print(f"   🔧  {info['functions']}")
    print(f"   🏗️  {info['material']}")
    print(f"   ⚖️  {info['weight']}")


# -------------------------------
# 11. Включение интерактивного выбора
# -------------------------------
plotter.enable_mesh_picking(callback=on_pick,
                            left_clicking=True,
                            show=True,
                            show_message=False)

# -------------------------------
# 12. Финальные настройки и запуск
# -------------------------------
plotter.show_grid(color='gray')
plotter.add_axes(color='black')

print("\n" + "=" * 60)
print("🚀  УПРАВЛЕНИЕ:")
print("   Shift + ЛКМ — выбрать деталь")
print("   ЛКМ + drag   — вращение камеры")
print("   ПКМ + drag   — панорама")
print("   Колёсико     — зум")
print("=" * 60)
print("💡  В ЛЕВОМ ВЕРХНЕМ УГЛУ — подробная информация о детали")
print("💡  ВНИЗУ — название выбранной детали")
print("💡  Каждая деталь подписана текстовой меткой")
print("=" * 60)

plotter.show()
print("\n👋  Завершено")
