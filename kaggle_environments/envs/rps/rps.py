import json
from os import path
from .agents import agents as all_agents

def check_action(player, weapons):
    if player.action is None:
        player.status = "INVALID"
        player.reward = 0
        return False

    if not isinstance(player.action, int) or player.action < 0 or player.action >= weapons:
        player.status = "INVALID"
        player.reward = 0
        return False
    return True

def update_player2_state(state):
    player1 = state[0].observation
    player2 = state[1].observation
    if 'opponent_last_score' in player1:
        player2.your_last_action = player1.opponent_last_action
        player2.your_last_score = player1.opponent_last_score
        player2.opponent_last_action = player1.your_last_action
        player2.opponent_last_score = player1.your_last_score
    player2.your_score = player1.opponent_score
    player2.opponent_score = player1.your_score
    player2.round = player1.round
    return state

def interpreter(state, env):
    player1 = state[0]
    player2 = state[1]
    if 'your_score' not in player1.observation:
      player1.observation.your_score = 0
      player1.observation.opponent_score = 0
      player1.observation.round = 0

    # Specification can fully handle the reset.
    if env.done:
        return update_player2_state(state)

    # Check for validity of actions
    player1_ok = check_action(player1, env.configuration.weapons)
    player2_ok = check_action(player2, env.configuration.weapons)
    player1.observation.your_last_action = player1.action
    player1.observation.opponent_last_action = state[1].action
    if not player1_ok or not player2_ok:
        if player1_ok:
            player1.status = "DONE"
            player1.reward = 1
        elif player2_ok:
            player2.status = "DONE"
            player2.reward = 1
        return update_player2_state(state)

    your_score = 0
    if (player1.action + player2.action) % 2 > 0:
        if (player1.action > player2.action):
            your_score = 1
        elif (player1.action < player2.action):
            your_score = 0
        else:
            your_score = 0.5
    else:
        if (player1.action < player2.action):
            your_score = 1
        elif (player1.action > player2.action):
            your_score = 0
        else:
            your_score = 0.5
    player1.observation.your_last_score = your_score
    player1.observation.opponent_last_score = 1 - your_score

    player1.observation.your_score += player1.observation.your_last_score
    player1.observation.opponent_score += player1.observation.opponent_last_score
    player1.observation.round += 1
    remaining_rounds = env.configuration.episodeSteps - player1.observation.round - 1
    if abs(player1.observation.your_score - player1.observation.opponent_score) > remaining_rounds:
        player1.reward = 1 if player1.observation.your_score > player1.observation.opponent_score else 0
        player1.status = "DONE"
        player2.reward = 1 - player1.reward
        player2.status = "DONE"
    elif remaining_rounds <= 0:
        player1.reward = 0.5
        player1.status = "DONE"
        player2.reward = 0.5
        player2.status = "DONE"

    return update_player2_state(state)


def renderer(state, env):
    weapon_name = ["Rock", "Paper", "Scissors", "Spock", "Lizard", "Airplane", "Sun", "Moon", "Camera", "Grass", "Fire", "Film", "Spanner", "Toilet", "School", "Air", "Death", "Planet", "Curse", "Guitar", "Lock", "Bowl", "Pickaxe", "Cup", "Peace", "Beer", "Computer", "Rain", "Castle", "Water", "Snake", "TV", "Blood", "Rainbow", "Porcupine", "UFO", "Eagle", "Alien", "Monkey", "Prayer", "King", "Mountain", "Queen", "Satan", "Wizard", "Dragon", "Mermaid", "Diamond", "Police", "Trophy", "Woman", "Money", "Baby", "Devil", "Man", "Link", "Home", "Video Game", "Train", "Math", "Car", "Robot", "Noise", "Heart", "Bicycle", "Electricity", "Tree", "Lightning", "Potato", "Ghost", "Duck", "Power", "Wolf", "Microscope", "Cat", "Nuke", "Chicken", "Cloud", "Fish", "Truck", "Spider", "Helicopter", "Bee", "Bomb", "Brain", "Tornado", "Community", "Sand", "Zombie", "Pit", "Bank", "Chain", "Vampire", "Gun", "Bath", "Law", "Monument", "Baloon", "Pancake", "Sword", "Book"]

    rounds_played = len(env.steps)
    board = ""

    # This line prints results each round, good for debugging
    for i in range(1, rounds_played):
        obs = env.steps[i][0].observation
        board = board + f"Round {i}: {weapon_name[obs.your_last_action]} vs {weapon_name[obs.opponent_last_action]}, Score: {obs.your_last_score} to {obs.opponent_last_score}\n"

    board = board + f"Game ended on round {rounds_played - 1}, final score: {state[0].observation.your_score} to {state[0].observation.opponent_score}\n"

    return board


dir_path = path.dirname(__file__)
json_path = path.abspath(path.join(dir_path, "rps.json"))
with open(json_path) as json_file:
    specification = json.load(json_file)


def html_renderer():
    js_path = path.abspath(path.join(dir_path, "rps.js"))
    with open(js_path, encoding="utf8") as js_file:
        return js_file.read()


agents = all_agents


weapons = {
    "Air": "💨",
    "Airplane": "✈️",
    "Alien": "👽",
    "Baby": "👶🏽",
    "Baloon": "🎈",
    "Bank": "🏦",
    "Bath": "🛁",
    "Bee": "🐝",
    "Beer": "🍺",
    "Bicycle": "🚲",
    "Blood": "💉",
    "Bomb": "💣",
    "Book": "📖",
    "Bowl": "🥣",
    "Brain": "🧠",
    "Camera": "📷",
    "Car": "🚗",
    "Castle": "🏰",
    "Cat": "🐈",
    "Chain": "⛓️",
    "Chicken": "🐓",
    "Cloud": "☁️",
    "Community": "👥",
    "Computer": "💻",
    "Cup": "☕",
    "Curse": "🥀",
    "Death": "☠",
    "Devil": "👹",
    "Diamond": "💎",
    "Dragon": "🐉",
    "Duck": "🦆",
    "Eagle": "🦅",
    "Electricity": "💡",
    "Film": "🎥",
    "Fire": "🔥",
    "Fish": "🐟",
    "Ghost": "👻",
    "Grass": "🌱",
    "Guitar": "🎸",
    "Gun": "🔫",
    "Heart": "❤️",
    "Helicopter": "🚁",
    "Home": "🏠",
    "King": "🤴🏼",
    "Law": "⚖️",
    "Lightning": "⚡",
    "Link": "🔗",
    "Lizard": "🦎",
    "Lock": "🔒",
    "Man": "👨🏾",
    "Math": "🔢",
    "Mermaid": "🧜🏽‍♀️",
    "Microscope": "🔬",
    "Money": "💰",
    "Monkey": "🐒",
    "Monument": "🏛️",
    "Moon": "🌙",
    "Mountain": "🏔️",
    "Noise": "🔔",
    "Nuke": "☢️",
    "Pancake": "🥞",
    "Paper": "📄",
    "Peace": "🕊️",
    "Pickaxe": "⛏️",
    "Pit": "🕳️",
    "Planet": "🌎",
    "Police": "👮🏽‍♀️",
    "Porcupine": "🦔",
    "Potato": "🥔",
    "Power": "🔋",
    "Prayer": "🙏🏽",
    "Queen": "👸🏽",
    "Rain": "🌧️",
    "Rainbow": "🌈",
    "Robot": "🤖",
    "Rock": "👊",
    "Sand": "🏖️",
    "Satan": "😈",
    "School": "🏫",
    "Scissors": "✂️",
    "Snake": "🐍",
    "Spanner": "🔧",
    "Spider": "🕷️",
    "Spock": "🖖",
    "Sun": "☀️",
    "Sword": "🗡️",
    "TV": "📺",
    "Toilet": "🚽",
    "Tornado": "🌪️",
    "Train": "🚂",
    "Tree": "🌲",
    "Trophy": "🏆",
    "Truck": "🚚",
    "UFO": "🛸",
    "Vampire": "🧛🏽‍♂️",
    "Video Game": "🎮",
    "Water": "💧",
    "Wizard": "🧙🏼‍♂️",
    "Wolf": "🐺",
    "Woman": "👩🏻",
    "Zombie": "🧟‍♂️"
}