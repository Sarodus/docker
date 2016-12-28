import click

from app.creator import CreatorApp
from app.extensions import db
app = CreatorApp()


@click.group()
def cli():
    pass

@cli.command()
def hello():
    print('Hello world')


@cli.command()
def create_db():
    with app.app_context():
        db.create_all()


@cli.command()
def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        make_dummy_seed()


@cli.command()
def seed_dummy():
    make_dummy_seed()


def make_dummy_seed():
    from app.models import Creation, Page, Component, Design
    
    with app.app_context():

        design = Design.query.filter_by(name='design1').first() or Design(name='design1')

        creation = Creation.query.filter_by(domain = 'creator').first() or Creation()
        creation.name = 'Dummy'
        creation.domain = 'creator'
        creation.active = True
        creation.design = design
        creation.menu = {
            'position': 'top',
            'links': [
                {'href':'/page1', 'name':'Media'},
                {'href':'/page2', 'name':'Poll'},
                {'href':'/page3', 'name':'My Page'},
            ]
        }


        db.session.add(creation)

        pages = (
            ('page1', (
                {'name':'TOP', 'type':'media', 'config':{'length':5}},
                {'name':'Twitter', 'type':'twitter', 'config':{'account_id':403614288}},
            )),
            ('page2', (
                {'name':'POLL Z', 'type':'poll', 'config':{'id_poll':123}},
            )),
            ('page3', (
                {'name':'History', 'type':'html', 'config':{'file':'custom_html_27.html'}},
            ))
        )

        for p, components in pages:
            page = Page.query.filter_by(creation = creation, name = p).first() or Page(name=p, creation=creation)
            db.session.add(page)

            for component in components:
                c = Component.query.filter_by(name = component['name'], page = page, type = component['type']).first() or Component()
                c.page = page
                c.name = component['name']
                c.type = component['type']
                c.config = component['config']
                db.session.add(c)

        db.session.commit()

if __name__ == '__main__':
    cli()