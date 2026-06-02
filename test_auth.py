import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret',
    })

    with app.app_context():
        db.create_all()
        user = User(name='Test Gebruiker', email='test@example.com', rol='trainer')
        user.set_password('geheim123')
        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_login_succes(client):
    """Login met correcte gegevens werkt."""
    response = client.post('/login/', data={
        'email': 'test@example.com',
        'password': 'geheim123',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Welkom terug' in response.get_data(as_text=True)


def test_login_verkeerd_wachtwoord(client):
    """Login met verkeerd wachtwoord geeft foutmelding."""
    response = client.post('/login/', data={
        'email': 'test@example.com',
        'password': 'fout',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Ongeldige inloggegevens' in response.get_data(as_text=True)


def test_login_onbekend_email(client):
    """Login met onbekend e-mailadres geeft foutmelding."""
    response = client.post('/login/', data={
        'email': 'bestaat@niet.nl',
        'password': 'geheim123',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Ongeldige inloggegevens' in response.get_data(as_text=True)


def test_logout(client):
    """Na inloggen en uitloggen is de sessie verwijderd."""
    client.post('/login/', data={
        'email': 'test@example.com',
        'password': 'geheim123',
    })

    response = client.get('/login/uitloggen', follow_redirects=True)

    assert response.status_code == 200
    assert 'uitgelogd' in response.get_data(as_text=True)


def test_na_login_sessie_actief(client):
    """Na succesvol inloggen is de gebruiker ingelogd (sessie actief)."""
    client.post('/login/', data={
        'email': 'test@example.com',
        'password': 'geheim123',
    })

    response = client.get('/dashboard/', follow_redirects=False)
    assert response.status_code == 200


def test_na_logout_sessie_verwijderd(client):
    """Na uitloggen wordt een beveiligde pagina geblokkeerd."""
    client.post('/login/', data={
        'email': 'test@example.com',
        'password': 'geheim123',
    })
    client.get('/login/uitloggen')

    response = client.get('/dashboard/', follow_redirects=False)
    assert response.status_code == 302


@pytest.fixture
def view_only_client(app):
    """Ingelogde testclient met rol view-only."""
    with app.app_context():
        user = User(name='View Only', email='viewonly@example.com', rol='view-only')
        user.set_password('geheim123')
        db.session.add(user)
        db.session.commit()

    client = app.test_client()
    client.post('/login/', data={
        'email': 'viewonly@example.com',
        'password': 'geheim123',
    })
    return client


def test_view_only_dashboard_toegankelijk(view_only_client):
    """View-only gebruiker kan het dashboard openen."""
    response = view_only_client.get('/dashboard/', follow_redirects=False)
    assert response.status_code == 200


def test_view_only_impact_toegankelijk(view_only_client):
    """View-only gebruiker kan de impactpagina openen."""
    response = view_only_client.get('/dashboard/impact', follow_redirects=False)
    assert response.status_code == 200


def test_view_only_sponsor_toevoegen_geblokkeerd(view_only_client):
    """View-only gebruiker krijgt 403 bij poging sponsor toe te voegen."""
    response = view_only_client.get('/sponsors/toevoegen', follow_redirects=False)
    assert response.status_code == 403


def test_view_only_sponsor_bewerken_geblokkeerd(view_only_client):
    """View-only gebruiker krijgt 403 bij poging sponsor te bewerken."""
    response = view_only_client.get('/sponsors/1/bewerken', follow_redirects=False)
    assert response.status_code == 403


def test_view_only_sponsor_verwijderen_geblokkeerd(view_only_client):
    """View-only gebruiker krijgt 403 bij poging sponsor te verwijderen."""
    response = view_only_client.post('/sponsors/1/verwijderen', follow_redirects=False)
    assert response.status_code == 403


def test_view_only_workshop_bewerken_geblokkeerd(view_only_client):
    """View-only gebruiker krijgt 403 bij poging workshop te bewerken."""
    response = view_only_client.get('/workshops/1/bewerken', follow_redirects=False)
    assert response.status_code == 403


def test_view_only_workshop_verwijderen_geblokkeerd(view_only_client):
    """View-only gebruiker krijgt 403 bij poging workshop te verwijderen."""
    response = view_only_client.post('/workshops/1/verwijderen', follow_redirects=False)
    assert response.status_code == 403


def test_view_only_gebruikers_geblokkeerd(view_only_client):
    """View-only gebruiker krijgt 403 bij gebruikersbeheer."""
    response = view_only_client.get('/gebruikers/', follow_redirects=False)
    assert response.status_code == 403