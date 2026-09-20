def test_login_success(client):
    response = client.post('/login', data={
        'username': 'john_doe',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome back, John Doe!' in response.data

def test_login_invalid_credentials(client):
    response = client.post('/login', data={
        'username': 'john_doe',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username/email or password.' in response.data

def test_register_new_customer(client):
    response = client.post('/register', data={
        'username': 'new_user',
        'email': 'new_user@example.com',
        'password': 'secretpassword',
        'confirm_password': 'secretpassword',
        'full_name': 'New Customer',
        'role': 'customer',
        'phone': '+8801999999999',
        'address': 'RUET Campus'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful' in response.data

def test_register_duplicate_username(client):
    response = client.post('/register', data={
        'username': 'john_doe',
        'email': 'different_email@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'full_name': 'Duplicate User',
        'role': 'customer'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'already registered' in response.data

def test_logout(client):
    client.post('/login', data={'username': 'john_doe', 'password': 'password123'})
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'logged out successfully' in response.data
