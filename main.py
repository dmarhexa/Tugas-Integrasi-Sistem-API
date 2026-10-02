# ===== 1. IMPORT =====
from fastapi import FastAPI, HTTPException  # FastAPI = kerangka API, HTTPException = pengirim pesan error (misal 404)
from pydantic import BaseModel              # dasar membuat "formulir" data yang divalidasi otomatis
from typing import Optional                 # menandai isian yang boleh kosong

# ===== 2. MEMBUAT APLIKASI =====
app = FastAPI()  # membangun aplikasi; nama "app" dipakai oleh semua decorator di bawah

# ===== 3. MODEL DATA =====
class Item(BaseModel):                  # formulir data mahasiswa
    nama: str                           # WAJIB diisi (tidak ada Optional dan tidak ada nilai bawaan)
    alamat: Optional[str] = None        # teks, boleh kosong
    ipk: Optional[float] = None         # angka desimal, boleh kosong; diisi "abc" -> error 422
    semester: Optional[int] = None      # angka bulat, boleh kosong
    hobi: Optional[str] = None          # teks, boleh kosong

# ===== 4. PENYIMPANAN SEMENTARA =====
items_db = {}  # dictionary kosong: kunci = ID, nilai = data mahasiswa; hilang saat server mati

# ===== 5. ROOT =====
@app.get("/")                           # GET ke alamat / dijalankan oleh fungsi di bawah
def read_root():
    return {"message": "Hallo selamat datang. Semoga harimu menyenangkan!"}  # dictionary -> otomatis jadi JSON

# ===== 6. CREATE =====
@app.post("/items/", status_code=201)   # POST ke /items/; 201 = "berhasil dan data baru dibuat"
async def create_item(item: Item):      # JSON dari klien divalidasi sesuai formulir Item
    item_id = len(items_db) + 1         # ID baru = jumlah data sekarang + 1
    items_db[item_id] = {"id": item_id, **item.dict()}
    # item.dict() = ubah objek jadi dictionary biasa
    # **          = tuangkan semua isinya ke dictionary baru
    # hasil: {"id": 1, "nama": "...", "alamat": "...", ...}, disimpan dengan ID sebagai kunci
    return {"message": f"Item created with ID: {item_id}", "item": items_db[item_id]}  # bukti ke klien

# ===== 7. READ =====
@app.get("/items/{item_id}")            # {item_id} = bagian alamat yang berubah-ubah (path parameter)
async def read_item(item_id: int):      # diambil dari alamat; ": int" = harus angka bulat
    if item_id in items_db:             # kalau ID ada...
        return {"item_id": item_id, "item": items_db[item_id]}  # ...kirim datanya
    else:                               # kalau tidak ada...
        raise HTTPException(status_code=404, detail="Item not found")  # ...hentikan dan kirim error 404

# ===== 8. UPDATE =====
@app.put("/items/{item_id}")            # PUT ke /items/3 misalnya
async def update_item(item_id: int, item: Item):  # item_id dari alamat, item (data baru) dari body JSON
    if item_id in items_db:
        items_db[item_id].update(item.dict(exclude_unset=True))
        # exclude_unset=True = hanya ambil field yang BENAR-BENAR dikirim klien
        # update()           = timpa nilai lama dengan nilai baru, field lain dibiarkan
        return {"message": f"Item with ID: {item_id} updated", "item": items_db[item_id]}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# ===== 9. DELETE =====
@app.delete("/items/{item_id}")         # DELETE ke /items/3 misalnya
async def delete_item(item_id: int):
    if item_id in items_db:
        deleted_item = items_db.pop(item_id)  # pop() = hapus dari dictionary SEKALIGUS mengembalikan isinya
        return {"message": f"Item with ID: {item_id} deleted", "item": deleted_item}
    else:
        raise HTTPException(status_code=404, detail="Item not found")