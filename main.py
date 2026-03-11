from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import os
import uuid
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional

# Load environment variables securely
load_dotenv()

app = FastAPI(title="City Transit Pass System", description="Amnex MaaS Backend")

# --- Database Connection ---
def get_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"), 
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    try:
        yield conn
    finally:
        conn.close()

# --- Helper Functions ---
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Pydantic Data Models ---
class UserRegister(BaseModel):
    name: str
    mobile: str
    email: str
    password: str
    role: str = "Commuter"

class UserLogin(BaseModel):
    mobile: str
    password: str

class PassPurchaseRequest(BaseModel):
    user_id: str
    pass_type_id: int

class ValidationRequest(BaseModel):
    pass_code: str
    transport_mode: str
    validator_id: str

# --- 1. Authentication Endpoints ---
@app.post("/api/auth/register", summary="Register new user") #
def register_user(user: UserRegister, db=Depends(get_db)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id FROM users WHERE mobile = %s OR email = %s", (user.mobile, user.email))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already exists")
        
    hashed_pw = hash_password(user.password)
    try:
        cursor.execute("""
            INSERT INTO users (name, mobile, email, password_hash, role)
            VALUES (%s, %s, %s, %s, %s) RETURNING id, name, role
        """, (user.name, user.mobile, user.email, hashed_pw, user.role))
        new_user = cursor.fetchone()
        db.commit()
        return {"message": "User registered successfully", "user": new_user}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.post("/api/auth/login", summary="User login") #
def login_user(user: UserLogin, db=Depends(get_db)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    hashed_pw = hash_password(user.password)
    cursor.execute("SELECT id, name, role FROM users WHERE mobile = %s AND password_hash = %s", (user.mobile, hashed_pw))
    db_user = cursor.fetchone()
    cursor.close()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user": db_user, "token": "mock_jwt_session_token"}

# --- 2. Pass Management Endpoints ---
@app.get("/api/passes/types", summary="List available pass types") #
def get_pass_types(db=Depends(get_db)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM pass_types")
    passes = cursor.fetchall()
    cursor.close()
    return passes

@app.post("/api/passes/purchase", summary="Purchase a pass") #
def purchase_pass(request: PassPurchaseRequest, db=Depends(get_db)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    
    # Get pass details to calculate expiry
    cursor.execute("SELECT validity_days FROM pass_types WHERE id = %s", (request.pass_type_id,))
    pass_type = cursor.fetchone()
    if not pass_type:
        raise HTTPException(status_code=404, detail="Pass type not found")
        
    expiry_date = datetime.now().astimezone() + timedelta(days=pass_type['validity_days'])
    pass_code = f"PASS-{uuid.uuid4().hex[:8].upper()}" # Generate unique code
    
    cursor.execute("""
        INSERT INTO user_passes (user_id, pass_type_id, pass_code, expiry_date)
        VALUES (%s, %s, %s, %s) RETURNING id, pass_code, expiry_date
    """, (request.user_id, request.pass_type_id, pass_code, expiry_date))
    
    new_pass = cursor.fetchone()
    db.commit()
    cursor.close()
    return {"message": "Pass purchased successfully", "pass": new_pass}

# --- 3. The Validation Engine ---
@app.post("/api/validate", summary="Validate a pass") #
def validate_pass(request: ValidationRequest, db=Depends(get_db)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("""
        SELECT up.id as user_pass_id, up.expiry_date, up.status, 
               pt.transport_modes, pt.max_trips_per_day
        FROM user_passes up
        JOIN pass_types pt ON up.pass_type_id = pt.id
        WHERE up.pass_code = %s
    """, (request.pass_code,))
    
    transit_pass = cursor.fetchone()
    if not transit_pass:
        raise HTTPException(status_code=404, detail="Pass not found")

    # Business Logic Checks
    if transit_pass['status'] == 'Expired' or transit_pass['expiry_date'] < datetime.now().astimezone():
        raise HTTPException(status_code=400, detail="Pass expired") #

    if request.transport_mode not in transit_pass['transport_modes']:
        raise HTTPException(status_code=400, detail="Transport mode not covered") #

    # Anti-passback check
    cursor.execute("SELECT validated_at FROM trips WHERE user_pass_id = %s ORDER BY validated_at DESC LIMIT 1", (transit_pass['user_pass_id'],))
    last_trip = cursor.fetchone()
    if last_trip:
        if datetime.now().astimezone() - last_trip['validated_at'] < timedelta(minutes=5):
            raise HTTPException(status_code=400, detail="Please wait before next validation") #

    # Daily trip limit check
    if transit_pass['max_trips_per_day'] is not None:
        cursor.execute("SELECT COUNT(*) as today_trips FROM trips WHERE user_pass_id = %s AND DATE(validated_at) = CURRENT_DATE", (transit_pass['user_pass_id'],))
        if cursor.fetchone()['today_trips'] >= transit_pass['max_trips_per_day']:
            raise HTTPException(status_code=400, detail="Daily trip limit reached") #

    # Record the trip
    cursor.execute("INSERT INTO trips (user_pass_id, validated_by, transport_mode) VALUES (%s, %s, %s)", (transit_pass['user_pass_id'], request.validator_id, request.transport_mode))
    db.commit()
    cursor.close()
    
    return {"status": "success", "message": "Valid"}

from typing import Optional

# --- 4. History and Admin Endpoints ---

@app.get("/api/trips/history", summary="Get trip history for a commuter")
def get_trip_history(user_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None, db=Depends(get_db)):
    """
    Fetch history showing date, time, transport mode, and route[cite: 47].
    Includes optional date range filtering[cite: 48].
    """
    cursor = db.cursor(cursor_factory=RealDictCursor)
    
    query = """
        SELECT t.transport_mode, t.route_info, t.validated_at, up.pass_code 
        FROM trips t
        JOIN user_passes up ON t.user_pass_id = up.id
        WHERE up.user_id = %s
    """
    params = [user_id]
    
    # Filter by date range if provided [cite: 48]
    if start_date and end_date:
        query += " AND DATE(t.validated_at) BETWEEN %s AND %s"
        params.extend([start_date, end_date])
        
    query += " ORDER BY t.validated_at DESC"
    
    cursor.execute(query, tuple(params))
    history = cursor.fetchall()
    cursor.close()
    
    return {"history": history}

@app.get("/api/admin/dashboard", summary="Admin statistics")
def get_admin_dashboard(db=Depends(get_db)):
    """
    Shows total passes sold (daily/weekly/monthly) and validations per mode[cite: 50, 51].
    """
    cursor = db.cursor(cursor_factory=RealDictCursor)
    
    # Total passes sold (daily/weekly/monthly) [cite: 50]
    cursor.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE purchase_date >= CURRENT_DATE) as daily_passes,
            COUNT(*) FILTER (WHERE purchase_date >= CURRENT_DATE - INTERVAL '7 days') as weekly_passes,
            COUNT(*) FILTER (WHERE purchase_date >= CURRENT_DATE - INTERVAL '30 days') as monthly_passes
        FROM user_passes
    """)
    passes_sold = cursor.fetchone()
    
    # Total validations per transport mode [cite: 51]
    cursor.execute("""
        SELECT transport_mode, COUNT(*) as total_validations
        FROM trips
        GROUP BY transport_mode
    """)
    validations_by_mode = cursor.fetchall()
    
    cursor.close()
    
    return {
        "passes_sold": passes_sold,
        "validations_by_mode": validations_by_mode
    }
    
