from distutils.core import setup

setup(
    name='Spooti',
    version='0.1dev',
    packages=['spooti',],
    install_requires=['spotipy'], #at some point we need to change this to just auto discover packages
)