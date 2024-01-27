from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_register():
    # delete all users
    response = client.get("/delete_all_users")
    response = client.post(
        "/gl/register",
        json={
            "username": "gltest",
            "password": "Password2g#",
            "team_name": "team1"
        }
    )
    print(response.json())
    assert response.status_code == 200

    # register player under gl
    response = client.post(
        "/gl/register_player",
        json={
            "gl_username": "gltest",
            "username": "player",
            "password": "Password2g#"
        }
    )
    print(response.json())
    assert response.status_code == 200
    # get all users
    response = client.get("/get_all_users")
    # login as player
    response = client.post(
        "/user/login",
        json={
            "username": "player",
            "password": "Password2g#"
        }
    )
    print(response.json())
    assert response.status_code == 200
    # change player password
    response = client.post(
        "/gl/change_player_password",
        json={
            "gl_username": "gltest",
            "username": "player",
            "new_password": "Password2g##"
        }
    )
    print(response.json())
    # login as player
    response = client.post(
        "/user/login",
        json={
            "username": "player",
            "password": "Password2g##"
        }
    )
    print(response.json())
    assert response.status_code == 200
    
    #delete all users
    response = client.get("/delete_all_users")
    assert response.status_code == 200

if __name__ == "__main__":
    test_read_main()
    test_register()