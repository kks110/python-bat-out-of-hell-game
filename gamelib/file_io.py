import fileinput
import os



# If the scores file doesnt exist, it creates it.
# Then appent the score to the file
def save_score(score):
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.isfile('data/top.scores'):
        f = open('data/top.scores', 'w')
        f.close()
    score = str(score)
    score = score + '\n'
    f = open('data/top.scores', 'a')
    f.write(score)
    f.close()

# Reads each line and saves to a list
# Turns them back to ints to sorts them correctly
# Returns the top 5 and changes back to string to be displayed
def load_scores():
    top_scores = []
    scores = [line.rstrip('\n') for line in open('data/top.scores')]
    scores = [int(x) for x in scores]
    scores.sort(reverse = True)
    top_scores = scores[:5]
    top_scores = [str(x) for x in top_scores]
    return top_scores
