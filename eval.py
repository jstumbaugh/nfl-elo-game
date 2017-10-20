from util import *
from forecast import *
from datetime import datetime
import csv

def frange(start, stop, step, places=1):
    i = start
    while(i <= stop):
        yield i
        i = round(i + step, places)

# Read historical games from CSV
games = Util.read_games("data/nfl_games.csv")

evaluations = []
start = datetime.now()

# Forecast every game
for hfa in range(101):
    for k in frange(0, 30, 0.1):
        for revert in frange(0.0, 1.0, 0.01, 2):
            Forecast.forecast(games, hfa, k, revert)

            avg = Util.evaluate_forecasts(games)
            evaluation = {"average": avg, "HFA": hfa, "K": k, "REVERT": revert}
            evaluations.append(evaluation)
    print "%s / 100" % hfa
    print str(datetime.now())

end = datetime.now()

with open('forecasts.csv', 'wb') as output_file:
    headers = evaluations[0].keys()
    dict_writer = csv.DictWriter(output_file, headers)
    dict_writer.writeheader()
    dict_writer.writerows(evaluations)

print "\n\n"
print "========================================================================"
print "\nFinished optimizing. Time taken: %s" % str(end - start)
print "\nWrote output to 'forecasts.csv'\n"

maximum = max(evaluations, key=lambda x:x['average'])
print "Maximum average was: %s" % (maximum['average'])
print "Inputs: %s\n" % maximum
print "========================================================================"
