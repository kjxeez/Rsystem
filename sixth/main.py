from flask import Flask, render_template, request
from engine import *
import pandas as pd
import random

app = Flask(__name__)

gamers = 5
probs = [1/7, 2/7, 1/7, 2/7, 1/7]


rounds = 20
blockchain = Blockchain()
accs = [20] * gamers
log = list()
trans_table = list()


def Game_start(probs, blockchain, game_round=1, number=4):
    print(accs)
    active = len(accs)
    total_of_trans = 0
    while game_round != 0:
        print("\nРаунд №", abs(game_round - 20) + 1)
        winner1 = random.choices(list(range(number)), weights=probs)
        winner = winner1[0]
        total = [0 for i in range(gamers)]
        for i in range(len(accs)):
            c_accs = accs
            c_accs.sort()
            min = c_accs[0]
            if accs[i] != 0:
                if i == winner:

                    blockchain.new_transaction("Gamer_" + str(winner), "Gamer_" + str(accs.index(min)), 1)
                    total_of_trans = total_of_trans + 1
                    if total_of_trans == 5:
                        mine(blockchain)
                        total_of_trans = 0
                    total_of_trans = total_of_trans + 1
                    if total_of_trans == 5:
                        mine(blockchain)
                        total_of_trans = 0

                    accs[accs.index(min)] = accs[accs.index(min)] + 2

                    total[winner] = total[winner] - 2
                    accs[winner] = accs[winner] - 2
                    accs[winner] = accs[winner] + active - 1
                    total[winner] = total[winner] + active - 1
                else:
                    blockchain.new_transaction("Gamer_" + str(i), "Gamer_" + str(winner), 1)
                    accs[i] = accs[i] - 1
                    total[i] = total[i] - 1
                    total_of_trans = total_of_trans + 1
                    if total_of_trans == 5:
                        mine(blockchain)
                        total_of_trans = 0
        trans_table.append(total)
        t = 0
        for i in trans_table:
            if i[winner] < 0:
                t = t + i[winner]
        log.append(f"Победил игрок {winner + 1} с начала игры он перевел: {t} монет")
        game_round = game_round - 1
    print("\nИтоговый балланс каждого из игроков: ", accs)
    mine(blockchain)


@app.route('/')
@app.route('/index')
def MainPage():
    df = pd.DataFrame(accs, columns=['Баланс'], index=[f"Игрок {i}" for i in range(1, gamers + 1)])
    df_html = df.to_html()
    return render_template("index.html", accs=df_html, gamers=gamers, probs=probs)


@app.route('/game')
def MainPageGame():
    Game_start(probs, blockchain, rounds, gamers)
    df = pd.DataFrame(accs, columns=['Баланс'], index=[f"Игрок {i}" for i in range(1, gamers + 1)])
    df_html = df.to_html()
    return render_template("index.html", accs=df_html, gamers=gamers, probs=probs)


@app.route('/bchn')
def MakeBlockchain():
    mine(blockchain)
    df = pd.DataFrame(accs, columns=['Баланс'], index=[f"Игрок {i}" for i in range(1, gamers + 1)])
    df_html = df.to_html()
    lb = get_end_block(blockchain)
    return render_template("index.html", accs=df_html, gamers=gamers, probs=probs, lb=lb)


@app.route('/rounds')
def GameLog():
    return render_template("rounds.html", log=log)


@app.route('/transfers')
def TransPage():
    df = pd.DataFrame(trans_table, columns=[f"Игрок {i}" for i in range(1, gamers + 1)],
                      index=[f"Раунд {i}" for i in range(1, rounds + 1)])
    df_html = df.to_html()
    return render_template("transfers.html", table=df_html)
if __name__ == '__main__':
    app.debug = True
    app.run()