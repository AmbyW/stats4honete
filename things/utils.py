import os
import time
import threading

NUM_WORKERS = 6


class ParserGame(object):
    match_id = ""
    server_game_name = ""
    game_name = ""
    game_version = ""
    match_name = ""
    map_name = ""
    map_version = ""
    match_date = ""
    match_time = ""
    team_win = ""
    win_time = 0
    playersgame_set = []
    delete_it = False
    delete_reazon = ""
    finished = False

    def __init__(self):
        match_id = ""
        server_game_name = ""
        game_name = ""
        game_version = ""
        match_name = ""
        map_name = ""
        map_version = ""
        match_date = ""
        match_time = ""
        team_win = ""
        win_time = 0
        playersgame_set = list()
        delete_it = False
        delete_reazon = ""
        finished = False

    def delete(self):
        for pg in self.playersgame_set:
            del pg
        del self


class ParserPlayerGame(object):
    ip_address = ""
    hero = ""
    player = ""
    player_pos = ""
    team = ""
    kills = 0
    dead = 0
    experiens = 0
    golds = 0
    assitances = 0
    damage = 0
    firstblood = 0
    firstblood_die = 0

    def __init__(self):
        ip_address = ""
        hero = ""
        player = ""
        player_pos = ""
        team = ""
        kills = 0
        dead = 0
        experiens = 0
        golds = 0
        assitances = 0
        damage = 0
        firstblood = 0
        firstblood_die = 0


def parse_info_game(line, storage):
    line_list = line.split("\"")
    storage.game_name = line_list[1]
    storage.game_version = line_list[3]


def parse_info_match(line, storage):
    line_list = line.split("\"")
    storage.match_name = line_list[1]
    storage.match_id = line_list[3]


def parse_info_map(line, storage):
    line_list = line.split("\"")
    storage.map_name = line_list[1]
    storage.map_version = line_list[3]


def parse_info_server(line, storage):
    line_list = line.split("\"")
    storage.server_game_name = line_list[1]


def parse_player_conn(line, storage):
    line_list1 = line.split("\"")
    line_list2 = line.split(":")
    player_pos = ''
    exist_player_conn = False
    for u in range(len(line_list2)):
        if 'player' in line_list2[u]:
            player_pos = line_list2[u+1].split(' ')[0]
            break
    for player_game in storage.playersgame_set:
        if player_game.player_pos == player_pos:
            exist_player_conn = True
            player_game.player = line_list1[1]
            player_game.ip_address = line_list1[3]
            break
    if not exist_player_conn:
        player = ParserPlayerGame()
        player.player = line_list1[1]
        player.player_pos = player_pos
        player.ip_address = line_list1[3]
        storage.playersgame_set.append(player)


def parse_teamchange(line, storage):
    line_list1 = line.split(":")
    team = line_list1[-1].replace('\n', '')
    player_pos = line_list1[1].split(' ')[0]
    player_exists = False
    for player in storage.playersgame_set:
        if player.player_pos == player_pos:
            player.team = team
            player_exists = True
            break
    if not player_exists:
        player = ParserPlayerGame()
        player.player_pos = player_pos
        player.team = team
        storage.playersgame_set.append(player)


def parse_kill(line, storage):
    who_kill = ''
    hero_kill = ''
    hero_die = ''
    who_die = ''
    killer_team = ''
    who_assist = []
    line_list1 = line.split(":")
    founded_killer = founded_dead = False
    for u in range(len(line_list1)):
        if 'player' in line_list1[u]:
            who_kill = line_list1[u+1].split(' ')[0]
        if 'owner' in line_list1[u]:
            who_die = line_list1[u+1].replace('\n', '').split(' ')[0]
        if 'team' in line_list1[u]:
            killer_team = line_list1[u+1].split(' ')[0]
        if 'assists' in line_list1[u]:
            who_assist = line_list1[u+1].replace('\n', '').split(',')
        if 'target' in line_list1[u]:
            hero_die = line_list1[u+1].replace('"', '').split(' ')[0]
        if 'attacker' in line_list1[u]:
            hero_kill = line_list1[u+1].replace('"', '').split(' ')[0]
    for player in storage.playersgame_set:
        if player.player_pos == who_kill:
            if hero_die.startswith('Hero_') and hero_kill.startswith('Hero_'):
                player.kills += 1
                player.hero = hero_kill
                player.team = killer_team
            founded_killer = True
        if player.player_pos == who_die:
            if hero_die.startswith('Hero_'):
                player.dead += 1
                player.hero = hero_die
                founded_dead = True
        if player.player_pos in who_assist:
            player.assitances += 1
    if not founded_killer and who_kill != '' and hero_kill.startswith('Hero_'):
        player_kill = ParserPlayerGame()
        player_kill.player_pos = who_kill
        player_kill.kills += 1
        player_kill.team = killer_team
        player_kill.hero = hero_kill
        storage.playersgame_set.append(player_kill)
    if not founded_dead and who_die != '' and hero_die.startswith('Hero_'):
        player_dead = ParserPlayerGame()
        player_dead.player_pos = who_die
        player_dead.dead += 1
        player_dead.hero = hero_die
        storage.playersgame_set.append(player_dead)


def parse_first(line, storage):
    line_list = line.split(":")
    player_pos = ''
    player_die_pos = ''
    hero_slug = ''
    player_team = ''
    first_time = ''
    founded_killer = founded_dead = False
    for u in range(len(line_list)):
        if 'time' in line_list[u]:
            first_time = line_list[u+1].split(' ')[0]
        if 'player' in line_list[u]:
            player_pos = line_list[u+1].split(' ')[0]
        if 'owner' in line_list[u]:
            player_die_pos = line_list[u+1].replace('\n', '').split(' ')[0]
        if 'name' in line_list[u]:
            hero_slug = line_list[u+1].replace('"', '').split(' ')[0]
        if 'team' in line_list[u]:
            player_team = line_list[u+1].split(' ')[0]
    if player_pos != '':
        for player in storage.playersgame_set:
            if player.player_pos == player_pos:
                player.firstblood = first_time
                player.hero = hero_slug
                founded_killer = True
            if player.player_pos == player_die_pos:
                player.firstblood_die = first_time
                founded_dead = True
            if founded_killer and founded_dead:
                break
        if not founded_killer and player_pos != '':
            player_kill = ParserPlayerGame()
            player_kill.team = player_team
            player_kill.player_pos = player_pos
            player_kill.hero = hero_slug
            storage.playersgame_set.append(player_kill)
        if not founded_dead and player_die_pos != '':
            player_die = ParserPlayerGame()
            player_die.player_pos = player_die_pos
            player_die.firstblood_die = first_time
            storage.playersgame_set.append(player_die)


def parse_gold_plus(line, storage):
    line_list = line.split(":")
    player_pos = ''
    gold = ''
    team = ''
    player_founded = False
    for u in range(len(line_list)):
        if 'player' in line_list[u]:
            player_pos = line_list[u+1].split(' ')[0]
        if 'gold' in line_list[u]:
            gold = line_list[u+1].split(' ')[0]
        if 'team' in line_list[u]:
            team = line_list[u+1].split(' ')[0]
    if player_pos != '':
        for player in storage.playersgame_set:
            if player.player_pos == player_pos:
                player.golds += int(gold)
                player.team = team
                player_founded = True
                break
        if not player_founded:
            player = ParserPlayerGame()
            player.player_pos = player_pos
            player.golds += int(gold)
            player.team = team
            storage.playersgame_set.append(player)


def parse_gold_less(line, storage):
    line_list = line.split(":")
    player_pos = ''
    gold = ''
    team = ''
    player_founded = False
    for u in range(len(line_list)):
        if 'player' in line_list[u]:
            player_pos = line_list[u+1].split(' ')[0]
        if 'gold' in line_list[u]:
            gold = line_list[u+1].split(' ')[0]
        if 'team' in line_list[u]:
            team = line_list[u+1].split(' ')[0]
    if player_pos != '':
        for player in storage.playersgame_set:
            if player.player_pos == player_pos:
                player.golds -= int(gold)
                player.team = team
                player_founded = True
                break
        if not player_founded:
            player = ParserPlayerGame()
            player.player_pos = player_pos
            player.golds -= int(gold)
            player.team = team
            storage.playersgame_set.append(player)


def parse_damage(line, storage):
    line_list = line.split(":")
    player_pos = ''
    damage = ''
    hero = ''
    team = ''
    player_founded = False
    for u in range(len(line_list)):
        if 'player' in line_list[u]:
            player_pos = line_list[u+1].split(' ')[0]
        if 'damage' in line_list[u]:
            damage = line_list[u+1].split(' ')[0].replace('\n', '')
        if 'attacker' in line_list[u]:
            hero = line_list[u+1].replace('"', '').split(' ')[0]
        if 'team' in line_list[u]:
            team = line_list[u+1].replace('"', '').split(' ')[0]
    if player_pos != '':
        for player in storage.playersgame_set:
            if player.player_pos == player_pos:
                player.hero = hero
                player.team = team
                player.damage += float(damage)
                player_founded = True
                break
        if not player_founded:
            player = ParserPlayerGame()
            player.player_pos = player_pos
            player.hero = hero
            player.team = team
            player.damage += float(damage)
            storage.playersgame_set.append(player)


def parse_exp(line, storage):
    line_list = line.split(":")
    player_pos = ''
    team = ''
    exp = ''
    player_founded = False
    for u in range(len(line_list)):
        if 'player' in line_list[u]:
            player_pos = line_list[u+1].split(' ')[0]
        if 'experience' in line_list[u]:
            exp = line_list[u+1].split(' ')[0].replace('\n', '')
        if 'team' in line_list[u]:
            team = line_list[u+1].split(' ')[0]
    if player_pos != '':
        for player in storage.playersgame_set:
            if player.player_pos == player_pos:
                player.experiens += float(exp)
                player.team = team
                player_founded = True
                break
        if not player_founded:
            player = ParserPlayerGame()
            player.team = team
            player.experiens += float(exp)
            player.player_pos = player_pos
            storage.playersgame_set.append(player)


def parse_datetime(line, storage):
    line_list = line.split("\"")
    date = line_list[1].replace("/", "-")
    time = line_list[3]
    storage.match_date = date
    storage.match_time = time


def parse_end(line, storage):
    print("parsing end line")
    line_list = line.split(":")
    duration = ""
    winner = ""
    for u in range(len(line_list)):
        if 'winner' in line_list[u]:
            winner = line_list[u+1].replace("\"", "").replace("\n", "")
        if 'time' in line_list[u]:
            duration = line_list[u+1].split(" ")[0]
    if winner != "":
        storage.team_win = winner
        storage.finished = True
    if duration != "":
        storage.win_time = duration
        storage.finished = True


def parse_start(last_lines, storage):
    for line in last_lines:
        if "GAME_END" in line:
            parse_end(line, storage)


def parse_data(data, storage, start=None, end=None):
    """
        :param data list()
        :param start integer
        :param end integer
        Esta funcion lo que hace es parsear o analizar una lista de lineas extraidas de un archivo Log de HoN y
        devuelve los objetos necesarios para poblar la base de datos
        :returns null|object
    """
    if not data:
        return
    if not start:
        start = 0
    if not end:
        end = len(data)

    start_time = time.time()
    for line in data[start:end]:
        if 'INFO_DATE' in line:
            parse_datetime(line, storage)
        if 'INFO_GAME' in line:
            parse_info_game(line, storage)
        if 'INFO_MATCH' in line:
            parse_info_match(line, storage)
        if 'INFO_MAP' in line:
            parse_info_map(line, storage)
        if 'INFO_SERVER' in line:
            parse_info_server(line, storage)
        if str(line).startswith('GAME_START'):
            parse_start(data[-4:], storage)
        if str(line).startswith('PLAYER_CONNECT'):
            parse_player_conn(line, storage)
        if str(line).startswith('PLAYER_TEAM_CHANGE'):
            parse_teamchange(line, storage)
        if str(line).startswith('KILL'):
            parse_kill(line, storage)
        if str(line).startswith('AWARD_FIRST_BLOOD'):
            parse_first(line, storage)
        if str(line).startswith('EXP_EARNED'):
            parse_exp(line, storage)
        if str(line).startswith('GOLD_EARNED'):
            parse_gold_plus(line, storage)
        if str(line).startswith('GOLD_LOST'):
            parse_gold_less(line, storage)
        if str(line).startswith('DAMAGE'):
            parse_damage(line, storage)
    end_time = time.time()
    print("Elapsed time=", end_time - start_time)
