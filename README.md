# Razzytails
---------

Razzytails is a game meant to be playable on the Raspberry Pi. You are
Razzy and you have to collect all of the items needed to get your
Raspberry Pi working. Sounds simple, but wait! Honey Badgers are dead
set on preventing you from getting your Raspberry Pi working. Avoid
them at all costs! If a Honey Badger catches you, then you still have
one more chance. Just answer a question about Python Programming and
you can shake the Honey Badger off your trail and continue your quest.

![Game Screenshot](http://i.imgur.com/WDXbxdq.png)

# Details
----------

Razzytails is built on top of [pygame](http://www.pygame.org/news.html).

## Installation

### OSX Mountain Lion

Installing pygame is *not* easy. Follow
[Julia Elman's excellent guide](http://juliaelman.com/blog/2013/04/02/installing-pygame-on-osx-mountain-lion/).

### Linux and Raspberry Pi

1. First, install pygame using your OS's tools (apt-get, yum, etc.).

        sudo apt-get install python-pygame

    N.B. Pygame comes with the raspbian distribution so you likely already have it for Raspberry Pi

2. Next, download the code

        git clone https://github.com/calebsmith/razzytails.git

3. Run the game

        cd razzytails
        ./main.sh

    or
        cd razzytails/src
        python main.py

4. Go help Razzy build your Raspberry Pi!!
