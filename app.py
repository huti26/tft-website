from flask import Flask, render_template, request

from autochess.ac_data import ACData
from autochess.ac_json import ACJson
from autochess.ac_simulation_analyzer import ACSimulationAnalyzer
from autochess.ac_calculator import tftUnluckCalc

app = Flask(__name__)

tft_game_data = ACData(game="tft-7.0")
tft_game_json = ACJson(game_data=tft_game_data)


@app.route('/calculator')
def calculator():
    return render_template(
        'ac_calculator.html'
    )


@app.route('/simulator')
def simulator():
    return render_template(
        'ac_simulator.html',
        game_data=tft_game_data
    )


@app.route('/explanation/calculator')
def explanation_calculator():
    return render_template(
        'ac_calculator_explanation.html'
    )


@app.route('/explanation/simulator')
def explanation_simulator():
    return render_template(
        'ac_simulator_explanation.html'
    )


@app.route('/')
def home():
    return render_template(
        'ac_home.html'
    )


@app.route('/api/tft/simulation', methods=['POST'])
def api_tft_simulation():
    data = request.json
    print("Request received")
    print(data)

    player_level = int(data["Player Level"])
    gold = int(data["Gold"])

    desired_champs, taken_champs = tft_game_json.seperate_data(data)

    desired_champ_pool = tft_game_json.desired_champs_from_json(desired_champs)

    starting_champ_pool = tft_game_json.champ_pool_from_json(taken_champs)

    print("Desired", desired_champ_pool)
    print("Pool", starting_champ_pool)

    result = ACSimulationAnalyzer(
        player_level=player_level,
        gold=gold,
        desired_champ_pool=desired_champ_pool,
        starting_champ_pool=starting_champ_pool,
        n=1000,
        game_data=tft_game_data
    ).analyze()

    # format output which is 0.889254 as an example
    result = result * 100
    result = f'{result:3.2f}%'

    return {'chance': result}


@app.route('/api/tft/calculation', methods=['POST'])
def api_tft_calculation():
    data = request.json
    print("Request received")
    print(data)

    champion_tier = int(data["tier"])
    player_level = int(data["level"])
    gold = int(data["gold"])
    champion_picked = int(data["champion_picked"])
    others_picked = int(data["others_picked"])

    is_dragon = False
    if "is_dragon" in data:
        is_dragon = True

    result = tftUnluckCalc(
        champion_tier,
        player_level,
        gold,
        champion_picked,
        others_picked,
        is_dragon,
        tft_game_data
    )

    # format output which is 0.889254 as an example
    result = result * 100
    result = f'{result:3.2f}%'

    return {'chance': result}


if __name__ == '__main__':
    app.run()
