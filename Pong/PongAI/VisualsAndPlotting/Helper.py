import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores_1, mean_scores_1, scores_2, mean_scores_2):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    #plt.plot(scores_1, label="score AI P1")  # for plotting the score of AI Player One
    plt.plot(mean_scores_1, label="mean score AI P1")
    #plt.plot(scores_2, label="score AI P2")  # for plotting the score of AI Player Two
    plt.plot(mean_scores_2, label="mean score AI P2") 
    plt.ylim(ymin=0)
    if mean_scores_1:
        plt.text(len(mean_scores_1)-1, mean_scores_1[-1], str(mean_scores_1[-1]))
    if mean_scores_2:
        plt.text(len(mean_scores_2)-1, mean_scores_2[-1], str(mean_scores_2[-1]))
    plt.show(block=False)
    plt.legend(loc='upper left')
    plt.pause(.1)
