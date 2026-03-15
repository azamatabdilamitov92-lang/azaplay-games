import streamlit as st
import random

st.set_page_config(page_title="AzaPlay Games", page_icon="🎮", layout="centered")
st.title("🎮 AzaPlay Games")

# Имя игрока
player = st.text_input("Введите имя игрока")

# Инициализация общих переменных
if "coins" not in st.session_state:
    st.session_state.coins = 0

if "hints_guess" not in st.session_state:
    st.session_state.hints_guess = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "hint_rps" not in st.session_state:
    st.session_state.hint_rps = False

if "hints_coinflip" not in st.session_state:
    st.session_state.hints_coinflip = 0

if "hints_anagram" not in st.session_state:
    st.session_state.hints_anagram = 0

# -------------------------
# Меню игр
# -------------------------
with st.sidebar:
    menu = st.radio(
        "Выберите игру",
        ["Главная", "Угадай число", "Камень Ножницы Бумага", "Орёл или Решка", "Анаграмма", "Магазин"]
    )

# -------------------------
# Главная страница
# -------------------------
if menu == "Главная":
    st.header("Добро пожаловать в AzaPlay Games!")
    st.write("Здесь будут мини-игры и таблица лучших игроков 🏆")
    st.write(f"Монеты: {st.session_state.coins} 🪙")

# -------------------------
# Игра "Угадай число"
# -------------------------
elif menu == "Угадай число":
    st.title("🎲 Угадай число")
    min_num, max_num = 1, 20
    number_to_guess = st.session_state.get("number_to_guess", random.randint(min_num, max_num))
    st.session_state.number_to_guess = number_to_guess

    guess = st.number_input(f"Угадайте число от {min_num} до {max_num}", min_value=min_num, max_value=max_num, step=1)
    if st.button("Проверить"):
        st.session_state.attempts += 1
        # Подсказка
        if st.session_state.hints_guess > 0:
            hint_chance = random.choice([True, False])
            if hint_chance:
                st.info(f"Подсказка: попробуйте число рядом с {number_to_guess}")
            st.session_state.hints_guess -= 1
        # Проверка
        if guess == number_to_guess:
            st.success(f"Вы угадали! 🎉 Попытки: {st.session_state.attempts}")
            st.session_state.coins += 1
            st.write(f"+1 монета! Монеты: {st.session_state.coins} 🪙")
            st.session_state.number_to_guess = random.randint(min_num, max_num)
            st.session_state.attempts = 0
        elif guess < number_to_guess:
            st.info("Слишком мало!")
        else:
            st.info("Слишком много!")

    st.write(f"Монеты: {st.session_state.coins} 🪙")
    st.write(f"Подсказки: {st.session_state.hints_guess}")

# -------------------------
# Камень-Ножницы-Бумага
# -------------------------
elif menu == "Камень Ножницы Бумага":
    st.title("✊ Камень-Ножницы-Бумага ✌️")
    choice = st.selectbox("Выберите ход", ["Камень", "Ножницы", "Бумага"])
    if st.button("Играть"):
        if st.session_state.hint_rps:
            hint = random.choice(["Камень", "Ножницы", "Бумага"])
            st.info(f"Подсказка: попробуй {hint}")
            st.session_state.hint_rps = False
        comp_choice = random.choice(["Камень", "Ножницы", "Бумага"])
        st.write(f"Компьютер выбрал: {comp_choice}")
        if choice == comp_choice:
            st.info("Ничья!")
        elif (choice=="Камень" and comp_choice=="Ножницы") or \
             (choice=="Ножницы" and comp_choice=="Бумага") or \
             (choice=="Бумага" and comp_choice=="Камень"):
            st.success("Вы выиграли! 🏆 +1 монета")
            st.session_state.coins += 1
        else:
            st.error("Вы проиграли 😢")
    st.write(f"Монеты: {st.session_state.coins} 🪙")

# -------------------------
# Орёл или Решка
# -------------------------
elif menu == "Орёл или Решка":
    st.title("🪙 Орёл или Решка")
    coin_choice = st.selectbox("Выберите сторону:", ["Орёл", "Решка"])
    if st.button("Бросить"):
        result = random.choice(["Орёл", "Решка"])
        if st.session_state.hints_coinflip > 0:
            hint_chance = random.choice([True, False])
            if hint_chance:
                st.info(f"Подсказка: монета скорее всего выпадет {result}")
            st.session_state.hints_coinflip -= 1
        if coin_choice == result:
            st.success(f"Вы выиграли! 🎉 Выпало {result}")
            st.session_state.coins += 1
        else:
            st.error(f"Вы проиграли. Выпало {result}")
    st.write(f"Монеты: {st.session_state.coins} 🪙")
    st.write(f"Подсказки: {st.session_state.hints_coinflip}")

# -------------------------
# Анаграмма
# -------------------------
elif menu == "Анаграмма":
    st.title("🔤 Анаграмма")
    word1 = st.text_input("Введите слово 1: ").lower()
    word2 = st.text_input("Введите слово 2: ").lower()
    if st.button("Проверить"):
        if sorted(word1) == sorted(word2) and word1 and word2:
            st.success("Это анаграмма!")
            st.session_state.coins += 0
        else:
            st.error("Не анаграмма 😢")
    st.write(f"Монеты: {st.session_state.coins} 🪙")
    st.write(f"Подсказки: {st.session_state.hints_anagram}")

# -------------------------
# Магазин
# -------------------------
elif menu == "Магазин":
    st.title("🛒 Магазин подсказок")
    st.write(f"Ваши монеты: {st.session_state.coins} 🪙")

    if st.button("Купить подсказку для 'Угадай число' (1 монета)"):
        if st.session_state.coins >= 1:
            st.session_state.coins -= 1
            st.session_state.hints_guess += 1
            st.success("Подсказка куплена!")
        else:
            st.error("Недостаточно монет!")

    if st.button("Купить подсказку для 'КНБ' (1 монета)"):
        if st.session_state.coins >= 1:
            st.session_state.coins -= 1
            st.session_state.hint_rps = True
            st.success("Подсказка куплена!")
        else:
            st.error("Недостаточно монет!")

    if st.button("Купить подсказку для 'Орёл/Решка' (1 монета)"):
        if st.session_state.coins >= 1:
            st.session_state.coins -= 1
            st.session_state.hints_coinflip += 1
            st.success("Подсказка куплена!")
        else:
            st.error("Недостаточно монет!")

    if st.button("Купить подсказку для 'Анаграмма' (1 монета)"):
        if st.session_state.coins >= 1:
            st.session_state.coins -= 1
            st.session_state.hints_anagram += 1
            st.success("Подсказка куплена!")
        else:
            st.error("Недостаточно монет!")