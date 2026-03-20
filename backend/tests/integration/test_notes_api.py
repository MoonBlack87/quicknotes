def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_notes_empty(client):
    response = client.get("/api/notes/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_note(client):
    response = client.post(
        "/api/notes/", json={"title": "My First Note", "content": "Hello!"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My First Note"
    assert data["content"] == "Hello!"
    assert data["pinned"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_note_empty_title_fails(client):
    response = client.post("/api/notes/", json={"title": ""})
    assert response.status_code == 422


def test_create_note_missing_title_fails(client):
    response = client.post("/api/notes/", json={"content": "No title"})
    assert response.status_code == 422


def test_create_note_content_too_long_fails(client):
    response = client.post(
        "/api/notes/",
        json={"title": "Too Long", "content": "a" * 1001},
    )
    assert response.status_code == 422


def test_list_notes_returns_created(client):
    client.post("/api/notes/", json={"title": "Note A"})
    client.post("/api/notes/", json={"title": "Note B"})
    response = client.get("/api/notes/")
    assert response.status_code == 200
    titles = [n["title"] for n in response.json()]
    assert "Note A" in titles
    assert "Note B" in titles


def test_list_notes_pinned_first(client):
    client.post("/api/notes/", json={"title": "Normal"})
    client.post("/api/notes/", json={"title": "Pinned", "pinned": True})
    notes = client.get("/api/notes/").json()
    assert notes[0]["title"] == "Pinned"


def test_update_note(client):
    create_resp = client.post("/api/notes/", json={"title": "Original"})
    note_id = create_resp.json()["id"]
    update_resp = client.patch(f"/api/notes/{note_id}", json={"title": "Updated"})
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "Updated"


def test_update_note_content_too_long_fails(client):
    note_id = client.post("/api/notes/", json={"title": "Original"}).json()["id"]
    response = client.patch(
        f"/api/notes/{note_id}",
        json={"content": "a" * 1001},
    )
    assert response.status_code == 422


def test_pin_note(client):
    note_id = client.post("/api/notes/", json={"title": "Pin Test"}).json()["id"]
    resp = client.patch(f"/api/notes/{note_id}", json={"pinned": True})
    assert resp.status_code == 200
    assert resp.json()["pinned"] is True


def test_update_nonexistent_note(client):
    response = client.patch("/api/notes/bad-id", json={"title": "X"})
    assert response.status_code == 404


def test_delete_note(client):
    note_id = client.post("/api/notes/", json={"title": "Bye"}).json()["id"]
    del_resp = client.delete(f"/api/notes/{note_id}")
    assert del_resp.status_code == 204
    notes = client.get("/api/notes/").json()
    assert all(n["id"] != note_id for n in notes)


def test_delete_nonexistent_note(client):
    response = client.delete("/api/notes/ghost")
    assert response.status_code == 404
