import click
from flask import g
from flask.cli import with_appcontext

from flaskr.models import models


def init_app(app):
    """
    app.teardown_appcontext() tells Flask to call that function when cleaning up after returning
    the response.
    app.cli.add_command() adds a new command that can be called with the flask command.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(reinit_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()


@click.command('reinit-db')
@with_appcontext
def reinit_db_command():
    for model in models:
        model.drop_table()
    click.echo("Cleared the database.")
    init_db()


def init_db():
    for model in models:
        click.echo(f"Initialize {model.name}")
        model.create_table()
        model.fill_table()
    click.echo('Database initialized.')


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
