# ===== 1. IMPORT =====
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


# ===== 2. MEMBUAT APLIKASI =====
app = FastAPI(
    title="API Mahasiswa",
    description="API untuk mengelola data mahasiswa",
    version="1.0.0",
)


# ===== 3. MODEL DATA MAHASISWA =====
class Mahasiswa(BaseModel):
    nama: str
    alamat: Optional[str] = None
    ipk: Optional[float] = None
    semester: Optional[int] = None
    hobi: Optional[str] = None


# ===== 4. PENYIMPANAN DATA =====
mahasiswa_db: dict[int, dict] = {}


# ===== 5. ROOT =====
@app.get("/")
def read_root():
    return {"message": "Halo Selamat datang! Have A Nice Day!"}


# ===== 6. CREATE / MENAMBAH DATA =====
@app.post("/mahasiswa/{mahasiswa_id}", status_code=201)
async def create_mahasiswa(mahasiswa_id: int, mahasiswa: Mahasiswa):

    if mahasiswa_id in mahasiswa_db:
        raise HTTPException(
            status_code=400,
            detail=f"ID mahasiswa {mahasiswa_id} sudah digunakan"
        )

    mahasiswa_db[mahasiswa_id] = mahasiswa.model_dump()

    return {
        "message": f"Mahasiswa created with ID: {mahasiswa_id}",
        "mahasiswa": mahasiswa_db[mahasiswa_id]
    }


# ===== 7. READ / MELIHAT DATA =====
@app.get("/mahasiswa/{mahasiswa_id}")
async def read_mahasiswa(mahasiswa_id: int):

    if mahasiswa_id in mahasiswa_db:
        return {
            "mahasiswa_id": mahasiswa_id,
            "mahasiswa": mahasiswa_db[mahasiswa_id]
        }

    raise HTTPException(status_code=404, detail="Mahasiswa not found")


# ===== 8. UPDATE / MENGUBAH DATA =====
@app.put("/mahasiswa/{mahasiswa_id}")
async def update_mahasiswa(mahasiswa_id: int, mahasiswa: Mahasiswa):

    if mahasiswa_id in mahasiswa_db:
        mahasiswa_db[mahasiswa_id] = mahasiswa.model_dump()
        return {
            "message": f"Mahasiswa with ID: {mahasiswa_id} updated",
            "mahasiswa": mahasiswa_db[mahasiswa_id]
        }

    raise HTTPException(status_code=404, detail="Mahasiswa not found")


# ===== 9. DELETE / MENGHAPUS DATA =====
@app.delete("/mahasiswa/{mahasiswa_id}")
async def delete_mahasiswa(mahasiswa_id: int):

    if mahasiswa_id in mahasiswa_db:
        deleted_mahasiswa = mahasiswa_db.pop(mahasiswa_id)
        return {
            "message": f"Mahasiswa with ID: {mahasiswa_id} deleted",
            "mahasiswa": deleted_mahasiswa
        }

    raise HTTPException(status_code=404, detail="Mahasiswa not found")