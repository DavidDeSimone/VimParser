import math
import string
import random
import vimhud
from os.path import expanduser

home = expanduser("~")
plugin_path = '/.vim/bundle/VimParser/plugin/'
usefullness_file_name= home + plugin_path + "usefullness.txt"
user_stats_file_name = home + plugin_path + "short_term.txt"
user_regexs_file_name = home + plugin_path + "long_term.txt"
command_description_file_name = home + plugin_path + "command.txt"
command_description_insert_file_name = home + plugin_path + "insert.txt"


def load_stats():
    usefulness = dict()
    user_stats = dict()
    load_usefull(usefulness)
    load_user_stats(user_stats)
    return usefulness, user_stats

def load_description():
    description = dict()
    desc = open(command_description_file_name, 'r')
    for line in desc:
        line = string.split(line, '\t')
        description[line[0]] = line[1]
    return description


def load_regex_stats(stats):
    stats_file = open(user_regexs_file_name, 'r')
    for line in stats_file:
        line = string.split(line, '\t')
        stats[line[0]] = int(line[1])


def load_usefull(usefulness):
    usefulness_file = open(usefullness_file_name, 'r')
    for line in usefulness_file:
        line = string.split(line, '\t')
        usefulness[line[0]] = int(line[1])

def load_user_stats(user_stats):
    user_stats_file = open(user_stats_file_name, 'r')
    for line in user_stats_file:
        line = string.split(line)
        user_stats[line[0]] = math.exp(-int(line[1])/150.0)#learn constant??


def combine_features(usefullness, user_stats, recent_stats):
    #assert(len(usefullness) == len(user_stats) and len(user_stats) == len(recent_stats))
    probabilities = list()
    for key in usefullness.keys():
        probabilities.append((50.0*usefullness[key])*recent_stats[key])

    #create a cdf for the (unweighted) probabilities
    for i in xrange(1, len(probabilities)):
        probabilities[i] = probabilities[i-1] + probabilities[i]
    #get uniform random number between 0, probabilites[len-1] to sample cdf
    rv = random.randint(0, probabilities[len(probabilities)-1])
    if rv <= probabilities[0]:
        return usefullness.keys()[0]
    for i in xrange(1, len(probabilities)-1):
        if probabilities[i-1] < rv and probabilities[i] >= rv:
            return usefullness.keys()[i]
    return usefullness.keys()[len(probabilities)-1]


def recommend():
    vimhud.update()
    usefullness, user_stats = load_stats()
    desc = load_description()
    recent_stats = usefullness
    random =  combine_features(usefullness, user_stats, recent_stats)
    try:
        return str(random) + ": " + str(desc[random])
    except:
        #some things dont have a description yet
        return recommend()




def main():
    usefullness, user_stats = load_stats()
    desc = load_description()
    recent_stats = usefullness
    random =  combine_features(usefullness, user_stats, recent_stats)
    print str(random) + ": " + str(desc[random])

if __name__ == "__main__":
    main()
