import getpass
import fileinput
import sys
import os.path

SRC = '/home/jfreilic/proj/filk/'

NUM_MOVIES = 10
uservotes = [0 for i in range(NUM_MOVIES)]
uservotes_original = [0 for i in range(NUM_MOVIES)]
totalvotes = [[0 for j in range(3)] for i in range(NUM_MOVIES)]

def register_user_vote(line, accumulator_func):
    words = line.split()
    if len(words)!=2:
        print 'Invalid command'
    else:
        try:
            movie = int(words[0])
            vote = int(words[1])
            if movie>=NUM_MOVIES or movie<0:
                print 'Invalid poll number'
            elif vote>2 or vote<0:
                print 'Invalid vote value' 
            else:
                accumulator_func(movie, vote)
        except ValueError:
            print 'Invalid argument: not a number'

def load_user_data(username):
    userfile = open(SRC+'userfiles/'+username, 'r')
    for line in userfile:
        register_user_vote(line, accumulate_user_vote)
    for i in range (NUM_MOVIES):
        uservotes_original[i] = uservotes[i]

def load_all_data(username):
    for filename in os.listdir(SRC+'userfiles'):
        if (filename!=username):
            userfile = open(SRC+'userfiles/'+filename, 'r')
            for line in userfile:
                register_user_vote(line, accumulate_total_votes)
            userfile.close

def accumulate_user_vote(index, vote):
    uservotes[index] = vote;

def accumulate_total_votes(index, vote):
    totalvotes[index][vote] = totalvotes[index][vote]+1

def list_movies():
    moviefile = open(SRC+'moviefiles/movies', 'r')
    i = 0;
    for line in moviefile:
        movie_1_vote = str(totalvotes[i][1]+int(uservotes[i]==1))
        movie_2_vote = str(totalvotes[i][2]+int(uservotes[i]==2))
        print str(i) + ': ' +line.strip() + ' : ' + movie_1_vote + ' - ' +movie_2_vote
        i = i+1
    moviefile.close()

def write_votes(username):
    userfile = open(SRC+'userfiles/'+username, 'w')
    for i in range(NUM_MOVIES):
        if uservotes[i] != 0:
            userfile.write(str(i)+' '+str(uservotes[i])+'\n')
    userfile.close()

def main():
    username = getpass.getuser()
    load_user_data(username)
    load_all_data(username)
    while True:
        try:
            user_input = raw_input('> ').strip()
            if user_input == 'list' or user_input == 'l':
                print ''
    	        list_movies()
                print ''
            elif user_input == 'quit' or user_input == 'q' or user_input == 'exit':
                write_votes(username)
                return
            elif user_input == 'help':
                print ''
                print 'Type list or l to list the current movie polls'
                print 'Type <poll number> <movie number> to vote for a movie in a poll'
                print 'A movie number of 0 means no preference, 1 means the first movie, 2 the second, etc.'
                print ''
            else:
                register_user_vote(user_input, accumulate_user_vote)
        except KeyboardInterrupt:
            write_votes(username)
            print ''
            return


if __name__ == '__main__':
    main()