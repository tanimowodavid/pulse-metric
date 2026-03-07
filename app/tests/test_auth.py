def test_register_user(client):
    # Define what we are sending
    user_data = {
        "email": "tester@example.com",
        "company_name": "Test Co",
        "password": "strongpassword123"
    }
    
    # Send the request
    response = client.post("/auth/register", json=user_data)
    
    # Assert (Verify) the results
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "tester@example.com"
    assert "id" in data
    # Ensure we are NOT returning the password
    assert "password" not in data
