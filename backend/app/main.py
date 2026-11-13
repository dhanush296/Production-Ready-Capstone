import json, logging, os, sqlite3, time
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl, field_validator

logging.basicConfig(level=os.getenv("LOG_LEVEL","INFO"),format="%(asctime)s %(levelname)s %(name)s %(message)s")
log=logging.getLogger("launchpad")
DB=Path(os.getenv("DATABASE_PATH","internships.db"))
SEED=[
("Frontend Developer Intern","Northstar Labs","Remote","Remote","Build accessible React interfaces with a product team.",'["React","JavaScript","CSS"]',"https://example.com/apply"),
("Data Analyst Intern","Metric Grove","Bengaluru, India","Hybrid","Explore product data and communicate useful insights.",'["SQL","Python","Excel"]',"https://example.com/apply"),
("Backend Engineering Intern","CloudHarbor","Chennai, India","On-site","Develop APIs, write tests and learn production practices.",'["Python","FastAPI","SQL"]',"https://example.com/apply")]
def dbconn():
    if str(DB)!=":memory:": DB.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(str(DB)); c.row_factory=sqlite3.Row; return c
def init_db():
    with dbconn() as c:
        c.execute("CREATE TABLE IF NOT EXISTS internships(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,company TEXT NOT NULL,location TEXT NOT NULL,mode TEXT NOT NULL,description TEXT NOT NULL,skills TEXT NOT NULL,apply_url TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        if c.execute("SELECT COUNT(*) FROM internships").fetchone()[0]==0:
            c.executemany("INSERT INTO internships(title,company,location,mode,description,skills,apply_url) VALUES(?,?,?,?,?,?,?)",SEED)
@asynccontextmanager
async def lifespan(app):
    init_db(); log.info("application_started"); yield; log.info("application_stopped")
app=FastAPI(title="LaunchPad Internship API",version="1.0.0",lifespan=lifespan)
origins=[x.strip() for x in os.getenv("CORS_ORIGINS","http://localhost:5173,http://localhost:8080").split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_methods=["GET","POST"],allow_headers=["Content-Type"])
@app.middleware("http")
async def request_log(request:Request,call_next):
    start=time.perf_counter(); response=await call_next(request)
    log.info("request method=%s path=%s status=%s duration_ms=%.2f",request.method,request.url.path,response.status_code,(time.perf_counter()-start)*1000)
    return response
class Listing(BaseModel):
    title:str=Field(min_length=3,max_length=100)
    company:str=Field(min_length=2,max_length=100)
    location:str=Field(min_length=2,max_length=100)
    mode:str=Field(pattern="^(Remote|Hybrid|On-site)$")
    description:str=Field(min_length=10,max_length=2000)
    skills:list[str]=Field(min_length=1,max_length=12)
    apply_url:HttpUrl
    @field_validator("apply_url")
    @classmethod
    def safe_url(cls,v):
        if urlparse(str(v)).scheme not in ("http","https"): raise ValueError("URL must use HTTP or HTTPS")
        return v
def serialize(row):
    item=dict(row); item["skills"]=json.loads(item["skills"]); return item
@app.get("/api/health")
def health():
    try:
        with dbconn() as c: c.execute("SELECT 1")
        return {"status":"ok","database":"connected"}
    except sqlite3.Error:
        log.exception("health_check_failed"); raise HTTPException(503,"Database unavailable")
@app.get("/api/internships")
def list_jobs(q:str=Query("",max_length=100),location:str=Query("",max_length=100),mode:str=Query("",pattern="^(|Remote|Hybrid|On-site)$")):
    sql="SELECT * FROM internships WHERE 1=1"; args=[]
    if q.strip():
        sql+=" AND (title LIKE ? OR company LIKE ? OR skills LIKE ? OR description LIKE ?)"; term="%"+q.strip()+"%"; args += [term]*4
    if location.strip(): sql+=" AND location LIKE ?"; args.append("%"+location.strip()+"%")
    if mode: sql+=" AND mode=?"; args.append(mode)
    sql+=" ORDER BY created_at DESC,id DESC"
    with dbconn() as c: rows=c.execute(sql,args).fetchall()
    return [serialize(r) for r in rows]
@app.post("/api/internships",status_code=201)
def create_job(payload:Listing):
    with dbconn() as c:
        cur=c.execute("INSERT INTO internships(title,company,location,mode,description,skills,apply_url) VALUES(?,?,?,?,?,?,?)",(payload.title.strip(),payload.company.strip(),payload.location.strip(),payload.mode,payload.description.strip(),json.dumps(payload.skills),str(payload.apply_url)))
        row=c.execute("SELECT * FROM internships WHERE id=?",(cur.lastrowid,)).fetchone()
    log.info("internship_created id=%s",cur.lastrowid); return serialize(row)
