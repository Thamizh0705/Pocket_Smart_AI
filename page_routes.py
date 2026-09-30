from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router=APIRouter(tags=["Pages"])
templates=Jinja2Templates(directory="app/templates")

@router.get("/",response_class=HTMLResponse)
def index(request:Request): return templates.TemplateResponse("index.html",{"request":request})

@router.get("/login",response_class=HTMLResponse)
def login_page(request:Request): return templates.TemplateResponse("login.html",{"request":request})

@router.get("/register",response_class=HTMLResponse)
def register_page(request:Request): return templates.TemplateResponse("register.html",{"request":request})

@router.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request): return templates.TemplateResponse("dashboard.html",{"request":request})

@router.get("/history",response_class=HTMLResponse)
def history_page(request:Request): return templates.TemplateResponse("history.html",{"request":request})

@router.get("/home",response_class=HTMLResponse)
def home_page(request:Request): return templates.TemplateResponse("planner_home.html",{"request":request})

@router.get("/party",response_class=HTMLResponse)
def party_page(request:Request): return templates.TemplateResponse("planner_party.html",{"request":request})

@router.get("/jewelry",response_class=HTMLResponse)
def jewelry_page(request:Request): return templates.TemplateResponse("planner_jewelry.html",{"request":request})
