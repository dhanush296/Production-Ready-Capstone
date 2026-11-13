from fastapi.testclient import TestClient
from app.main import app
def test_health_and_seeded_jobs():
    with TestClient(app) as c:
        assert c.get("/api/health").json()["status"]=="ok"
        assert len(c.get("/api/internships").json())>=3
def test_search():
    with TestClient(app) as c:
        r=c.get("/api/internships",params={"q":"React"})
        assert r.status_code==200 and len(r.json())>=1
def test_invalid_mode_rejected():
    d={"title":"QA Intern","company":"Acme","location":"Remote","mode":"Other","description":"Test application workflows.","skills":["QA"],"apply_url":"https://example.com"}
    with TestClient(app) as c: assert c.post("/api/internships",json=d).status_code==422
def test_create_listing():
    d={"title":"QA Intern","company":"Acme Labs","location":"Remote","mode":"Remote","description":"Test application workflows and APIs.","skills":["QA","Python"],"apply_url":"https://example.com/apply"}
    with TestClient(app) as c:
        r=c.post("/api/internships",json=d); assert r.status_code==201 and r.json()["title"]=="QA Intern"
