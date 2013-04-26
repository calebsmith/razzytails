# Razzytails
---------

Razzytails is a game meant to be playable on the Raspberry Pi. You are
Razzy and you have to collect all of the items needed to get your
Raspberry Pi working. Sounds simple, but wait! Honey Badgers are dead
set on preventing you from getting your Raspberry Pi working. Avoid
them at all costs! If a Honey Badger catches you, then you still have
one more chance. Just answer a question about Python Programming and
you can shake the Honey Badger off your trail and continue your quest.


# Details
----------

Razzytails is built on top of [pygame](http://www.pygame.org/news.html).

## Installation

### OSX Mountian Lion

Installing pygame is *not* easy. Follow
[Julia Elman's excellent guide](http://juliaelman.com/blog/2013/04/02/installing-pygame-on-osx-mountain-lion/).

### Linux

1. First, install pygame using your OS's tools (apt-get, yum, etc.).

        sudo apt-get install pygame

2. Then, because I love virtualenvs, create a virtualenv that uses the
system site packages, so that it has access to the pygame that we just
installed:

        mkvirtualenv -p /usr/bin/python2 --system-site-packages razzytails

3. Next, download the code

        git clone https://github.com/juliaelman/razzytails.git

4. Run the game

        cd razzytails
        python main.py

5. Go build your Raspberry Pi!!
