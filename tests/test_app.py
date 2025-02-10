import os
import shutil
import tempfile
import pytest
from fastapi.testclient import TestClient
from app.main import app
from config import INPUT_DIR, OUTPUT_DIR

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    original_input_dir = INPUT_DIR
    original_output_dir = OUTPUT_DIR
    temp_input_dir = tempfile.mkdtemp()
    temp_output_dir = tempfile.mkdtemp()
    os.environ["INPUT_DIR"] = temp_input_dir
    os.environ["OUTPUT_DIR"] = temp_output_dir
    yield
    shutil.rmtree(temp_input_dir)
    shutil.rmtree(temp_output_dir)
    os.environ["INPUT_DIR"] = original_input_dir
    os.environ["OUTPUT_DIR"] = original_output_dir

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Bienvenue sur l'API ArchimindAI" in response.json()["message"]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_upload_csv():
    csv_content = "col1,col2,col3\n1,2,3\n4,5,6\n7,8,9"
    files = {"file": ("test.csv", csv_content, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "uploadé" in data["message"]

def test_report_endpoints():
    pptx_path = os.path.join(os.environ["OUTPUT_DIR"], "ArchiMindAI_Report.pptx")
    html_path = os.path.join(os.environ["OUTPUT_DIR"], "ArchiMindAI_Report.html")
    with open(pptx_path, "w") as f:
        f.write("Dummy PPTX content")
    with open(html_path, "w") as f:
        f.write("<html>Dummy HTML content</html>")
    
    response_pptx = client.get("/report/pptx")
    assert response_pptx.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.presentationml.presentation" in response_pptx.headers["content-type"]
    
    response_html = client.get("/report/html")
    assert response_html.status_code == 200
    assert "text/html" in response_html.headers["content-type"]

def test_files_listing():
    input_file = os.path.join(os.environ["INPUT_DIR"], "dummy.csv")
    output_file = os.path.join(os.environ["OUTPUT_DIR"], "dummy_report.html")
    with open(input_file, "w") as f:
        f.write("dummy")
    with open(output_file, "w") as f:
        f.write("dummy")
    response = client.get("/files")
    assert response.status_code == 200
    data = response.json()
    assert "dummy.csv" in data["input_data"]
    assert "dummy_report.html" in data["output"]

def test_dashboard_endpoint():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "<title>ArchimindAI Dashboard</title>" in response.text

def test_ai_commentary_endpoint():
    response = client.get("/ai/commentary")
    assert response.status_code == 200
    data = response.json()
    assert "commentary" in data

def test_payment_endpoints():
    response_stripe = client.post("/payment/stripe")
    assert response_stripe.status_code == 200
    data_stripe = response_stripe.json()
    assert "url" in data_stripe
    
    response_coinbase = client.post("/payment/coinbase")
    assert response_coinbase.status_code == 200
    data_coinbase = response_coinbase.json()
    assert "url" in data_coinbase
