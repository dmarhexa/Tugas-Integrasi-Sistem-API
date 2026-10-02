# ===== 1. IMPORT =====

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Bagian ini digunakan untuk mengambil library yang diperlukan.
# FastAPI untuk membuat API, BaseModel untuk membuat format data,
# dan HTTPException untuk menangani error.


# ===== 2. MEMBUAT APLIKASI =====

app = FastAPI(
    title="API Mahasiswa",
    description="API untuk mengelola data mahasiswa",
)

# Membuat aplikasi FastAPI yang nantinya digunakan
# untuk menjalankan semua endpoint.


# ===== 3. MODEL DATA MAHASISWA =====

class Mahasiswa(BaseModel):
    nama: str
    alamat: Optional[str] = None
    ipk: Optional[float] = None
    semester: Optional[int] = None
    hobi: Optional[str] = None

# Bagian ini menentukan data mahasiswa yang akan digunakan.
# ID dan nama wajib diisi, sedangkan alamat, IPK, semester,
# dan hobi boleh dikosongkan.


# ===== 4. PENYIMPANAN DATA =====

mahasiswa_db = {}

# Data mahasiswa disimpan sementara di dictionary.
# Data akan hilang jika server dimatikan.


# ===== 5. ROOT =====

@app.get("/")
def read_root():
    return {"message": "Halo Selamat datang! Have A Nice Day!"}

# Endpoint ini hanya digunakan untuk menampilkan
# pesan selamat datang ketika API dibuka.


# ===== 6. CREATE / MENAMBAH DATA =====

@app.post("/mahasiswa/", status_code=201)
async def create_mahasiswa(mahasiswa: Mahasiswa):

    if mahasiswa.id in mahasiswa_db:
        raise HTTPException(
            status_code=400,
            detail="ID mahasiswa sudah digunakan"
        )

    mahasiswa_db[mahasiswa.id] = mahasiswa.dict()

    return {
        "message": f"Mahasiswa created with ID: {mahasiswa.id}",
        "mahasiswa": mahasiswa_db[mahasiswa.id]
    }

# Endpoint POST digunakan untuk menambahkan mahasiswa.
# ID dimasukkan secara manual oleh pengguna.
# Jika ID sudah digunakan, maka akan muncul error 400.


# ===== 7. READ / MELIHAT DATA =====

@app.get("/mahasiswa/{mahasiswa_id}")
async def read_mahasiswa(mahasiswa_id: int):

    if mahasiswa_id in mahasiswa_db:
        return {
            "mahasiswa_id": mahasiswa_id,
            "mahasiswa": mahasiswa_db[mahasiswa_id]
        }

    else:
        raise HTTPException(
            status_code=404,
            detail="Mahasiswa not found"
        )

# Endpoint GET digunakan untuk melihat data mahasiswa
# berdasarkan ID. Jika ID tidak ditemukan, muncul error 404.


# ===== 8. UPDATE / MENGUBAH DATA =====

@app.put("/mahasiswa/{mahasiswa_id}")
async def update_mahasiswa(
    mahasiswa_id: int,
    mahasiswa: Mahasiswa
):

    if mahasiswa_id in mahasiswa_db:
        mahasiswa_db[mahasiswa_id] = mahasiswa.dict()

        return {
            "message": f"Mahasiswa with ID: {mahasiswa_id} updated",
            "mahasiswa": mahasiswa_db[mahasiswa_id]
        }

    else:
        raise HTTPException(
            status_code=404,
            detail="Mahasiswa not found"
        )

# Endpoint PUT digunakan untuk mengubah data mahasiswa.
# Data lama akan diganti dengan data yang baru.
# Jika ID tidak ditemukan, muncul error 404.


# ===== 9. DELETE / MENGHAPUS DATA =====

@app.delete("/mahasiswa/{mahasiswa_id}")
async def delete_mahasiswa(mahasiswa_id: int):

    if mahasiswa_id in mahasiswa_db:
        deleted_mahasiswa = mahasiswa_db.pop(mahasiswa_id)

        return {
            "message": f"Mahasiswa with ID: {mahasiswa_id} deleted",
            "mahasiswa": deleted_mahasiswa
        }

    else:
        raise HTTPException(
            status_code=404,
            detail="Mahasiswa not found"
        )

# Endpoint DELETE digunakan untuk menghapus data mahasiswa
# berdasarkan ID. Jika ID tidak ditemukan, muncul error 404.