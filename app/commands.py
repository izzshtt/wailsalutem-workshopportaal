import click
from flask.cli import with_appcontext
from app import db
from app.models.user import User


@click.command('seed')
@with_appcontext
def seed():
    accounts = [
        {'name': 'Admin Test', 'email': 'admin@test.nl', 'password': 'Admin123!', 'rol': 'admin'},
        {'name': 'Trainer Test', 'email': 'trainer@test.nl', 'password': 'Trainer123!', 'rol': 'trainer'},
    ]
    for data in accounts:
        if User.query.filter_by(email=data['email']).first():
            click.echo(f"Al aanwezig: {data['email']}")
            continue
        user = User(name=data['name'], email=data['email'], rol=data['rol'])
        user.set_password(data['password'])
        db.session.add(user)
        click.echo(f"Aangemaakt: {data['email']}")
    db.session.commit()
