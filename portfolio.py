import requests
import json

def save_data(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)

def load_data(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return{}

def add_coin(name, amount):
    portfolio = load_data("portfolio.json")
    if name in portfolio:
        portfolio[name] += amount
    else:
        portfolio[name] = amount
    save_data(portfolio, "portfolio.json")

def get_price(coin):
    url= f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json() 
    return data[coin]["usd"]

def show_portfolio():
    portfolio = load_data("portfolio.json")
    total = 0
    for coin in portfolio:
        try:
            price = get_price(coin)
        except KeyError:
            print(f"Не удалось получить цену {coin}, пропускаю")
            continue
        value = price * portfolio[coin]
        total += value
        print(f"{coin}: {portfolio[coin]} x ${price} = ${round(value, 2)}")
    print(f"Всего: ${round(total, 2)}")

while True:
    print("Добавить монету - 1")
    print("Показать портфель - 2")
    print("Выйти - 3")
    choice = input("Выберите: ")

    if choice == "1":
        name = input("Впишите название монеты: ").strip().lower()
        text = input("Количество монеты: ")
        try:
            amount = float(text.replace(",", "."))
        except ValueError:
            print("Нужно ввести число, например 0.5")
            continue
        if amount <= 0:
            print("Число должно быть больше нуля")
            continue
        add_coin(name, amount)
        
    elif choice == "2":
        show_portfolio()
    elif choice == "3":
        break
    else:
        print("Нет такого варианта выбора")



