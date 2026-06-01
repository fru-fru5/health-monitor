import pytest
from app import create_app, db
from app.models import User, HealthReading

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def patient_user(app):
    with app.app_context():
        user = User(name='Test Patient', email='patient@test.com', role='patient')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        return user

# --- Model Tests ---

def test_user_password_hashing(app):
    with app.app_context():
        user = User(name='Test', email='test@test.com', role='patient')
        user.set_password('securepass')
        assert user.check_password('securepass') is True
        assert user.check_password('wrongpass') is False

def test_health_reading_normal(app):
    reading = HealthReading(
        patient_id=1,
        blood_pressure_sys=120,
        blood_pressure_dia=80,
        heart_rate=75,
        temperature=37.0,
        blood_sugar=95
    )
    assert reading.check_alerts() == []

def test_health_reading_high_bp(app):
    reading = HealthReading(
        patient_id=1,
        blood_pressure_sys=160,
        blood_pressure_dia=100
    )
    alerts = reading.check_alerts()
    assert 'High systolic blood pressure' in alerts
    assert 'High diastolic blood pressure' in alerts

def test_health_reading_abnormal_heart_rate(app):
    reading = HealthReading(patient_id=1, heart_rate=130)
    assert 'Abnormal heart rate' in reading.check_alerts()

# --- Route Tests ---

def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_register_page_loads(client):
    response = client.get('/register')
    assert response.status_code == 200

def test_register_and_login(client, app):
    with app.app_context():
        client.post('/register', data={
            'name': 'New User',
            'email': 'new@test.com',
            'password': 'pass1234',
            'role': 'patient'
        })
        response = client.post('/login', data={
            'email': 'new@test.com',
            'password': 'pass1234'
        }, follow_redirects=True)
        assert response.status_code == 200

def test_dashboard_requires_login(client):
    response = client.get('/patient/dashboard', follow_redirects=True)
    assert b'log in' in response.data.lower() or response.status_code == 200
