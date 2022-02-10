[![Gitter](https://badges.gitter.im/DroidGame/DroidGame3D.svg)](https://gitter.im/WennMarcoRTX/MarcoEngine?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=body_badge) 

# MarcoEngine(WIP)

*Marco Engine* - Marco Engine is an interesting neural chess network that uses a self-learning method (achieving a good game by trying out mistakes). Technically, his rating is **3320**. Although, we are sure that this is not the maximum rating.


# ↓ Installation

First, install the required *libraries*:

```
pip install -r requirements.txt
```

Wait for the modules to be installed. Now, you need to set the weights. You can find out more about this in the __Where I can download weights?__ section.

# 🚗 Start engine

To run the engine, you must have weights. If you don't have weights, you can create a `weights_norm.json` file in the __weights__ folder. After that, go to the main directory of the project, then write the command:

```
python3 train.py
```

After that, wait the amount of time you need, and turn off the program. Congratulations! You now have a working __MarcoEngine__ in your hands. Time to test it. The engine supports a small part of the __UCI__ protocol, but this is enough. To start the UCI shell:

```
python3 uci.py [uci-commad](not necessary)
```

# 🖥️ Where I can download weights?
You can get the weights in two ways: 1. Download from one of the releases of __MarcoEngine__ (they will be in this repository), then transfer the weights file to the `weights` folder. Next, read the text under the heading __Start engine__ to understand how to start the engine. Method 2: train a neural network on a computer. If you want to generate weights directly on your computer, you can enter the command:

```
python3 train.py
```

Then wait some time for the training program to reach at least the first stage of weights. You can either continue the program to train, or just turn it off. After that, your path lies in the __Start engine__ header, where you will be shown how to start the engine.

# ⚙️ How does Marco Engine work?

__MarcoEngine__ uses the usual self-learning algorithms of a chess neural network: it simply learns from its mistakes. That is why you should not deform the `game[number].json` files, which contain the game on which the engine will be trained.

# 😄 Can I support project?

__Yes__. You can support the author by simply following his profile on *Lichess*: [click me](https://lichess.org/@/ProshkaKartoshka)!

Have a nice day, good learning! 😉
