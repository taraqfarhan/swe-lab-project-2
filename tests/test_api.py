def test_api_health(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'healthy'
    assert json_data['process_model'] == 'Kanban'

def test_api_restaurants(client):
    response = client.get('/api/v1/restaurants')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['count'] >= 3

def test_api_restaurant_menu(client):
    response = client.get('/api/v1/restaurants/1/menu')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['restaurant'] == 'Bella Italia'
    assert len(json_data['items']) >= 4

def test_api_order_status(client):
    response = client.get('/api/v1/orders/1')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['status'] == 'delivered'

def test_api_kanban_metrics(client):
    response = client.get('/api/v1/kanban/metrics')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert 'avg_lead_time_minutes' in json_data['metrics']
