# Pong with board edge physics

## Required libraries
For the application to run properly, please install following packages
<ul>
    <li>IPython</li>
    <li>matplotlib.pyplot</li>
    <li>numpy</li>
    <li>pygam</li>
    <li>random</li>
    <li>collections</li>
    <li>torch</li>
    <li>torch.nn</li>
    <li>torch.optim</li>
    <li>torch.nn.functiona</li>
    <li>os</li>
</ul>

## Game setup 
Everyone knows the game pong. I tried to code this WITH board edge physics.
<img src="https://github.com/BurakKTopal/SmallPythonProjects/blob/main/Pong/Media/BoardEdgePhysics.gif" alt="Pong GIF" height=200>

With the code provided in <a href="https://github.com/BurakKTopal/SmallPythonProjects/blob/main/Pong/Main.py">main</a>, you can play against a friend.
</p>

<p>Besides, I tried to make Reinforcement deep Q-learning, with inspiration of my earlier made <a href="https://github.com/BurakKTopal/SmallPythonProjects/tree/main/SnakeGame">SnakeGame</a>. With <a href="https://github.com/BurakKTopal/SmallPythonProjects/blob/main/Pong/PongAI/TrainingHumanToBot.py">TrainingHumanAgainstBot</a>, you yourself can try the bot to play better pong, but I shall warn you: it takes 100 - 120 games until the bot can play some decent pong. This may come due to the low learning rate, or other hyperparameters.
</p>

 <p>
     With <a href="https://github.com/BurakKTopal/SmallPythonProjects/blob/main/Pong/PongAI/TrainingBotAgainstBot.py">TrainingBotAgainstBot</a> you can look at how the bots learn to play pong themselves. The visualisations of their scores are done by <a href="https://github.com/BurakKTopal/SmallPythonProjects/blob/main/Pong/PongAI/VisualsAndPlotting/Helper.py">Helper.py</a>
 </p>

