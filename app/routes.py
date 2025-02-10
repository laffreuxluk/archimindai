import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from app.pipeline import run_analysis
from config import INPUT_DIR, OUTPUT_DIR
from app.payments import create_stripe_session, create_coinbase_charge
from app.ai_commentary import generate_commentary

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers CSV sont acceptés.")
    file_path = os.path.join(INPUT_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    if background_tasks:
        background_tasks.add_task(run_analysis, file_path)
    else:
        run_analysis(file_path)
    return {"message": f"Fichier '{file.filename}' uploadé et analyse lancée."}

@router.get("/report/pptx")
async def download_pptx():
    report_path = os.path.join(OUTPUT_DIR, "ArchiMindAI_Report.pptx")
    if os.path.exists(report_path):
        return FileResponse(report_path, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", filename="ArchiMindAI_Report.pptx")
    raise HTTPException(status_code=404, detail="Rapport PPTX non trouvé.")

@router.get("/report/html")
async def download_html_report():
    report_path = os.path.join(OUTPUT_DIR, "ArchiMindAI_Report.html")
    if os.path.exists(report_path):
        return FileResponse(report_path, media_type="text/html", filename="ArchiMindAI_Report.html")
    raise HTTPException(status_code=404, detail="Rapport HTML non trouvé.")

@router.get("/files")
async def list_files():
    input_files = os.listdir(INPUT_DIR) if os.path.exists(INPUT_DIR) else []
    output_files = os.listdir(OUTPUT_DIR) if os.path.exists(OUTPUT_DIR) else []
    return {"input_data": input_files, "output": output_files}

@router.post("/payment/stripe")
async def stripe_payment():
    session_url = create_stripe_session()
    return {"url": session_url}

@router.post("/payment/coinbase")
async def coinbase_payment():
    charge_url = create_coinbase_charge()
    return {"url": charge_url}

@router.get("/dashboard")
async def dashboard():
    dashboard_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>ArchimindAI Dashboard</title>
      <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
      <h1>Dashboard Interactif ArchimindAI</h1>
      <div id="dashboard"></div>
      <script>
        var data = [{
          x: [1, 2, 3, 4],
          y: [10, 15, 13, 17],
          type: 'scatter'
        }];
        Plotly.newPlot('dashboard', data);
      </script>
      <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="ca-pub-xxxxxxxxxxxxxxxx"
           data-ad-slot="yyyyyyyyyy"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
      <script>
           (adsbygoogle = window.adsbygoogle || []).push({});
      </script>
    </body>
    </html>
    """
    return HTMLResponse(content=dashboard_html, status_code=200)

@router.get("/ai/commentary")
async def ai_commentary():
    commentary = generate_commentary()
    return {"commentary": commentary}
