import json
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from ..config import settings
from ..database import get_connection
from ..dependencies import get_current_user
from ..gemini_utils import generate_recommendations
from ..models import User
from ..schemas import HomeRequest, PartyRequest

router = APIRouter(prefix="/api", tags=["Recommendations"])

def save_history(user_id:int, planner:str, data:dict, result:dict):
    conn=get_connection()
    try:
        cur=conn.execute("INSERT INTO recommendation_history(user_id,planner,budget,request_json,response_json) VALUES(?,?,?,?,?)",(user_id,planner,int(data["budget"]),json.dumps(data),json.dumps(result)))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

@router.post("/generate-home")
def generate_home(data: HomeRequest, user:User=Depends(get_current_user)):
    payload=data.model_dump()
    result=generate_recommendations("home",payload)
    result["id"]=save_history(user.id,"home",payload,result)
    return result

@router.post("/generate-party")
def generate_party(data: PartyRequest, user:User=Depends(get_current_user)):
    payload=data.model_dump()
    result=generate_recommendations("party",payload)
    result["id"]=save_history(user.id,"party",payload,result)
    return result

@router.post("/generate-jewelry")
async def generate_jewelry(
    budget:int=Form(...), occasion:str=Form(...), style:str=Form("Elegant"), metal:str=Form("Any"), outfit_description:str=Form(""), outfit_image:UploadFile|None=File(None), user:User=Depends(get_current_user)
):
    if budget <= 0:
        raise HTTPException(status_code=422, detail="Budget must be greater than zero")
    image_bytes=None
    mime_type=None
    if outfit_image and outfit_image.filename:
        allowed={"image/jpeg","image/png","image/webp"}
        if outfit_image.content_type not in allowed:
            raise HTTPException(status_code=415, detail="Use JPG, PNG or WebP image")
        image_bytes=await outfit_image.read()
        if len(image_bytes) > settings.max_image_mb*1024*1024:
            raise HTTPException(status_code=413, detail="Image is too large")
        mime_type=outfit_image.content_type
    payload={"budget":budget,"occasion":occasion,"style":style,"metal":metal,"outfit_description":outfit_description}
    result=generate_recommendations("jewelry",payload,image_bytes,mime_type)
    result["id"]=save_history(user.id,"jewelry",payload,result)
    return result

@router.get("/session-info")
def session_info(user:User=Depends(get_current_user)):
    return {"logged_in":True,"user_id":user.id,"name":user.name,"email":user.email}

@router.get("/session-data")
def session_data(user:User=Depends(get_current_user)):
    conn=get_connection()
    try:
        count=conn.execute("SELECT COUNT(*) AS c FROM recommendation_history WHERE user_id=?",(user.id,)).fetchone()["c"]
    finally:
        conn.close()
    return {"recommendation_count":count}

@router.get("/history")
def history(user:User=Depends(get_current_user)):
    conn=get_connection()
    try:
        rows=conn.execute("SELECT id,planner,budget,created_at,response_json FROM recommendation_history WHERE user_id=? ORDER BY id DESC LIMIT 50",(user.id,)).fetchall()
    finally:
        conn.close()
    return [{"id":r["id"],"planner":r["planner"],"budget":r["budget"],"created_at":r["created_at"],"summary":json.loads(r["response_json"]).get("summary","")} for r in rows]

@router.get("/recommendations-details/{recommendation_id}")
def recommendation_details(recommendation_id:int,user:User=Depends(get_current_user)):
    conn=get_connection()
    try:
        row=conn.execute("SELECT * FROM recommendation_history WHERE id=? AND user_id=?",(recommendation_id,user.id)).fetchone()
    finally:
        conn.close()
    if row is None:
        raise HTTPException(status_code=404,detail="Recommendation not found")
    result=json.loads(row["response_json"])
    result.update({"id":row["id"],"planner":row["planner"],"budget":row["budget"]})
    return result
