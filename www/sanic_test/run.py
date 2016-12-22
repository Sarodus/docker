import socket
import os
import click

from app.base import app
from scripts.random_users import get_random_users
from app.db import Base, engine, Session
from app.models import User

SOCK_FILE = '/var/run/sanic.sock'

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove(SOCK_FILE)
except OSError:
    pass
sock.bind(SOCK_FILE)


@click.group()
def cli():
    pass

@cli.command()
def runserver():
    app.run(sock=sock, host=None, port=None, workers=4, debug=True)


@cli.command()
@click.option('--number', default=10, type=click.IntRange(1, 1000))
def fill_db(number):
    sess = Session()
    sess.add_all(get_random_users(number))
    sess.commit()


@cli.command()
def create_db():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    cli()