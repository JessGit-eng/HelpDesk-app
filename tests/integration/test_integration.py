from fastapi.testclient import TestClient
from backend import main as backend_main
from main import app

client = TestClient(app)


def test_ticket_saved_to_database():

    # Prepare the ticket data:
    ticket = {
        "title": "VPN Issue",
        "description": "Cannot connect to VPN from home",
        "category": "network"
    }

    # Send the request to the API
    response = client.post("/tickets", data=ticket)

    # Assert vrify the API responded successfully:
    assert response.status_code == 200
    assert response.json()["id"]

def test_get_tickets():
    response = client.get("/tickets")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_ai_triage_response(monkeypatch):
    monkeypatch.setattr(
        backend_main,
        "triage_ticket",
        lambda *_: (
            "Priority: High\n"
            "Confidence: 90%\n"
            "Reason: The test AI recommendation."
        ),
    )

    ticket = {
        "title": "VPN Issue",
        "description": "Cannot connect to VPN from home",
        "category": "network"
    }
    create_response = client.post("/tickets", data=ticket)
    assert create_response.status_code == 200

    ticket_id = create_response.json()["id"]
    response = client.post(f"/tickets/{ticket_id}/triage")

    assert response.status_code == 200
    result = response.json()
    assert isinstance(result["priority"], str)
    assert result["priority"].strip()
    assert isinstance(result["confidence"], str)
    assert result["confidence"].strip()
    assert isinstance(result["reason"], str)
    assert result["reason"].strip()