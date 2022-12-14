import argparse
import datetime
import json
import logging
import math
import os
import re
import sys

failure=False
def warn(message):
    global failure
    failure = True
    logging.warning(message)

def get(ogsdata, field, default=None, logifnone=False, game_id=None):
  if field in ogsdata:
    return ogsdata[field]
  if logifnone:
    game_id = game_id or ogsdata.get("game_id") or "Unknown"
    warn(f"JSON field not found for game {game_id}: {field}")
  return default

def get_sgf(game_id, sgf, field, default=None, logifnone=False):
    m = re.search(field + '''\[([^][]+)\]''', sgf)
    if m:
        assert m.group(1)
        return m.group(1)
    if logifnone:
        warn(f"SGF field not found for game {game_id or 'Unknown'}: {field}")
    return default

def rankstr(rank):
  # glicko -> kyudan
  # if rank <= 0.0:
  #   rank = 1e-30
  # rank = math.log(rank/850.0)/0.032

  if rank >= 30.0:
    danrank = min(9,int(math.floor(rank) - 29))
    return f"{danrank}d"
  else:
    kyurank = min(30,int(30-math.floor(rank)))
    return f"{kyurank}k"

sgfescapetable = str.maketrans({"]":"\\]"})
def sgfescape(s):
  return s.translate(sgfescapetable)

sgfletters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def param(key, contents):
  contents = sgfescape(str(contents))
  return f"{key}[{contents}]"

def construct_sgf(ogsdata):
  global failure
  failure = False
  out = ""
  out += "(;FF[4]CA[UTF-8]GM[1]US[lightvector/ogstosgf.py]"
  extra_info = []

  game_id = get(ogsdata,"game_id",logifnone=True)
  if game_id is not None:
    out += param("PC",f"OGS: https://online-go.com/game/{game_id}")
  if game_id is None:
    game_id = "Unknown"

  time = get(ogsdata,"start_time")
  if time is not None:
    date = datetime.datetime.utcfromtimestamp(time)
    strdate = date.strftime('%Y-%m-%d')
    out += param("DT",strdate)

  players = get(ogsdata,"players",logifnone=True)
  black_username = None
  white_username = None
  if players is not None:
    black = get(players,"black",logifnone=True,game_id=game_id)
    white = get(players,"white",logifnone=True,game_id=game_id)
    if black is not None and len(black) > 0:
      black_username = get(black,"username",logifnone=True,game_id=game_id)
      if black_username is not None:
        out += param("PB",black_username)

    if white is not None and len(white) > 0:
      white_username = get(white,"username",logifnone=True,game_id=game_id)
      if white_username is not None:
        out += param("PW",white_username)

    if black is not None and len(black) > 0:
      black_rank = get(black,"rank",logifnone=False,game_id=game_id)
      if black_rank is not None:
        out += param("BR",rankstr(black_rank))

    if white is not None and len(white) > 0:
      white_rank = get(white,"rank",logifnone=False,game_id=game_id)
      if white_rank is not None:
        out += param("WR",rankstr(white_rank))

  original_sgf = get(ogsdata,"original_sgf")
  if original_sgf is not None:
    strdate = get_sgf(game_id, original_sgf, "DT")
    if strdate is not None:
        try:
            date = datetime.datetime.strptime(strdate, "%Y-%M-%d")
        except ValueError:
            pass

    black_username = get_sgf(game_id, original_sgf, "PB") or black_username
    white_username = get_sgf(game_id, original_sgf, "PW") or white_username
    return True, (black_username, white_username, date, game_id), original_sgf

  game_name = get(ogsdata,"game_name")
  if game_name is not None:
    out += param("GN",game_name)

  time_control = get(ogsdata,"time_control")
  if time_control is not None:
    system = get(time_control,"time_control")
    if system is None:
      system = get(time_control,"system")
    if system is None:
      system = get(time_control,"time_control",logifnone=True,game_id=game_id)

    if system == "byoyomi":
      main_time = get(time_control,"main_time",logifnone=True,game_id=game_id)
      period_time = get(time_control,"period_time",logifnone=True,game_id=game_id)
      periods = get(time_control,"periods",logifnone=True,game_id=game_id)
      if main_time is not None and period_time is not None and periods is not None:
        out += param("TM",main_time)
        out += param("OT",f"{periods}x{period_time} byo-yomi")
    elif system == "fischer":
      initial_time = get(time_control,"initial_time",logifnone=True,game_id=game_id)
      time_increment = get(time_control,"time_increment",logifnone=True,game_id=game_id)
      if initial_time is not None and time_increment is not None:
        out += param("TM",initial_time)
        out += param("OT",f"{time_increment} fischer")
    elif system == "simple":
      per_move = get(time_control,"per_move",logifnone=True,game_id=game_id)
      if per_move is not None:
        out += param("TM",0)
        out += param("OT",f"{per_move} simple")
    elif system == "canadian":
      main_time = get(time_control,"main_time",logifnone=True,game_id=game_id)
      period_time = get(time_control,"period_time",logifnone=True,game_id=game_id)
      stones_per_period = get(time_control,"stones_per_period",logifnone=True,game_id=game_id)
      if main_time is not None and period_time is not None and stones_per_period is not None:
        out += param("TM",main_time)
        out += param("OT",f"{stones_per_period}/{period_time} canadian")
    elif system == "absolute":
      total_time = get(time_control,"total_time",logifnone=True,game_id=game_id)
      if total_time is not None:
        out += param("TM",total_time)
    elif system == "none":
      pass
    else:
      warn(f"Unknown time control for game {game_id}: {system}")

    speed = get(time_control,"speed")
    if speed is not None:
      extra_info.append(speed)
    elif system == "none":
      extra_info.append("none")
    else:
      extra_info.append("unknown")

  winner = get(ogsdata,"winner")
  outcome = get(ogsdata,"outcome")
  if winner is not None or outcome is not None:
    white_player_id = get(ogsdata,"white_player_id",logifnone=True)
    black_player_id = get(ogsdata,"black_player_id",logifnone=True)
    if outcome == "0 points":
      out += param("RE","Draw")
    elif outcome and not winner:
      out += param("RE","Void")
    else:
      assert outcome
      assert winner
      if winner == white_player_id:
        winner = "W"
      elif winner == black_player_id:
        winner = "B"
      else:
        warn(f"Unknown winner for game {game_id}")
        winner = None
      if winner is not None:
        if outcome.endswith(" points"):
          out += param("RE",f"{winner}+{outcome[:-7]}")
        elif outcome == "1 point":
          out += param("RE",f"{winner}+1")
        elif outcome == "Resignation":
          out += param("RE",f"{winner}+R")
        elif outcome == "Timeout":
          out += param("RE",f"{winner}+T")
        elif outcome == "Cancellation":
          out += param("RE",f"{winner}+F")
        elif outcome == "Disconnection":
          out += param("RE",f"{winner}+F")
        elif outcome in ("Moderator Decision", "Decision", "Disqualification","Ladder Withdrawn"):
          out += param("RE",f"{winner}+F")
        else:
          warn(f"Unknown outcome (with known winner) for game {game_id}")
          out += param("RE","?")
      else:
          warn(f"Unknown outcome (with unknown winner) for game {game_id}")
          out += param("RE","?")
  else:
    out += param("RE","?") # Unfinished

  width = get(ogsdata,"width",default=19,logifnone=True)
  height = get(ogsdata,"height",default=19,logifnone=True)
  if width != height:
    out += param("SZ",f"{width}:{height}")
  else:
    out += param("SZ",width)

  komi = get(ogsdata,"komi",logifnone=True)
  if komi is not None:
    out += param("KM",komi)

  rules = get(ogsdata,"rules",logifnone=True)
  if rules is not None:
    if rules.lower() == "chinese":
      out += param("RU","Chinese")
    elif rules.lower() == "japanese":
      out += param("RU","Japanese")
    elif rules.lower() == "korean":
      out += param("RU","Korean")
    elif rules.lower() == "nz":
      out += param("RU","NZ")
    elif rules.lower() == "aga":
      out += param("RU","AGA")
    elif rules.lower() == "ing":
      out += param("RU","Ing")
    else:
      out += param("RU",rules)

  handicap = get(ogsdata,"handicap",default=0)
  if handicap > 0:
    out += param("HA",handicap)

  ranked = get(ogsdata,"ranked",default=False,logifnone=True)
  if ranked:
    extra_info.append("ranked")
  else:
    extra_info.append("unranked")

  out += param("GC",",".join(extra_info))

  initial_player = get(ogsdata,"initial_player")
  if initial_player is not None:
    if initial_player == "black":
      pass
    elif initial_player == "white":
      out += param("PL","W")
    else:
      warn(f"Unknown initial player for game {game_id}")
      initial_player = "black"
  else:
    initial_player = "black"

  initial_state = get(ogsdata,"initial_state")
  if initial_state is not None:
    bstate = get(initial_state,"black",logifnone=True,game_id=game_id)
    wstate = get(initial_state,"white",logifnone=True,game_id=game_id)
    if bstate is not None and len(bstate) > 0:
      out += "AB"
      for i in range(0, len(bstate), 2):
        out += "[" + bstate[i:i+2] + "]"
    if wstate is not None and len(wstate) > 0:
      out += "AW"
      for i in range(0, len(wstate), 2):
        out += "[" + wstate[i:i+2] + "]"

  moves = get(ogsdata,"moves",logifnone=True)
  if moves is not None:
    blacknext = True if initial_player == "black" else False
    for idx,data in enumerate(moves):
      if idx < handicap:
        if idx == 0:
          out += "AB"
        out += "[" + sgfletters[data[0]] + sgfletters[data[1]] + "]"
        if idx == handicap-1:
          blacknext = False
      else:
        if blacknext:
          out += ";B["
        else:
          out += ";W["
        if data[0] < 0 or data[1] < 0: # pass
          pass
        else:
          out += sgfletters[data[0]] + sgfletters[data[1]]
        out += "]"
        blacknext = not blacknext

  out += ")"
  out += "\n"
  #assert not failure, "Game {} failed to parse".format(game_id)
  if not failure:
    return False, (black_username, white_username, date, game_id), out

if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', stream = sys.stdout, level=logging.INFO)

  parser = argparse.ArgumentParser(description='Convert ogs jsons to sgfs')
  parser.add_argument('dirs', metavar='DIR', nargs='+', help='Directories of ogs json files')
  parser.add_argument('-verbose', required=False, action="store_true", help='Text file with npzs to ignore, one per line')

  args = parser.parse_args()

  num_processed = 0
  for arg in args.dirs:
    for (path,dirnames,filenames) in os.walk(arg, followlinks=True):
      filenames = [os.path.join(path,filename) for filename in filenames if filename.endswith('.json')]
      for filename in filenames:
        outfile = filename[:-5]+".sgf"
        if args.verbose:
          logging.info(f"{filename} -> {outfile}")
        with open(filename, encoding='UTF-8') as f:
          ogsdata = json.load(f)
        sgf = construct_sgf(ogsdata)
        with open(outfile,"w", encoding='UTF-8') as f:
          try:
            f.write(sgf[2])
          except BaseException as err:
            print("Exception raised at game_id", ogsdata['game_id'])
            print(type(err), ":", err)
        num_processed += 1
        if num_processed % 10000 == 0:
          logging.info(f"Processed {num_processed} files")

  logging.info(f"Processed {num_processed} files")
  logging.info("Done")