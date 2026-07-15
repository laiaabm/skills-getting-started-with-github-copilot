from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_available_activities():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_activity in payload
    assert "participants" in payload[expected_activity]


def test_signup_and_unregister_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    activity = activities_response.json()[activity_name]
    assert email not in activity["participants"]


def test_duplicate_signup_returns_error():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate.student@example.edu"

    # Act
    first_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_signup = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_signup.status_code == 200
    assert second_signup.status_code == 400
    assert second_signup.json()["detail"] == "Student already signed up for this activity"
