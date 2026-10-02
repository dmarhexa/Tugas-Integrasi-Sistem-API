# ===== 1. IMPORT: mengambil alat yang dibutuhkan =====
from fastapi import FastAPI, HTTPException  # FastAPI = kerangka API, HTTPException = pengirim pesan error (misal 404)
from pydantic import BaseModel              # dasar untuk membuat "formulir" data yang divalidasi otomatis
from typing import Optional                 # menandai bahwa sebuah isian boleh kosong

# ===== 2. MEMBUAT APLIKASI =====
app = FastAPI()  # membangun aplikasinya; nama "app" dipakai di semua decorator di bawah

# ===== 3. MODEL DATA: bentuk "formulir" mahasiswa =====
class Item(BaseModel):                # class Item mewarisi BaseModel, jadi otomatis punya validasi
    nama: Optional[str] = None        # teks, boleh kosong; kalau tidak diisi nilainya None
    alamat: Optional[str] = None      # teks, boleh kosong
    ipk: Optional[float] = None       # angka desimal (misal 3.75); kalau diisi teks "abc" -> error 422
    semester: Optional[int] = None    # angka bulat (misal 5)
    hobi: Optional[str] = None        # teks, boleh kosong

# ===== 4. PENYIMPANAN DATA SEMENTARA =====
items_db: dict[int, dict] = {}  # dictionary kosong: kunci = ID (int), nilai = data mahasiswa (dict)
                                # hilang saat server dimatikan karena hanya ada di memori
next_id = 1                     # penghitung ID; hanya naik, tidak pernah turun, jadi ID tidak pernah ganda

# ===== 5. ENDPOINT ROOT: cek API hidup =====
@app.get("/")                   # decorator: "request GET ke alamat / dijalankan oleh fungsi di bawah"
def read_root():                # nama fungsi bebas
    return {"message": "Hallo selamat datang. Semoga harimu menyenangkan!"}  # dictionary -> otomatis jadi JSON

# ===== 6. CREATE: tambah data baru =====
@app.post("/items/", status_code=201)  # method POST ke /items/; 201 = "berhasil dan data baru dibuat"
def create_item(item: Item):           # data JSON dari klien dibaca dan divalidasi sebagai objek Item
    global next_id                     # izin mengubah variabel next_id yang ada di luar fungsi
    item_id = next_id                  # ambil nomor ID yang akan dipakai sekarang
    next_id += 1                       # naikkan penghitung untuk data berikutnya
    items_db[item_id] = {"id": item_id, **item.model_dump()}
    # model_dump() = ubah objek item jadi dictionary biasa
    # **  = "tuangkan semua isi dictionary ini ke sini"
    # hasilnya: {"id": 1, "nama": "...", "alamat": "...", ...}, lalu disimpan dengan ID sebagai kunci
    return {"message": f"Item created with ID: {item_id}", "item": items_db[item_id]}  # kirim bukti ke klien

# ===== 7. READ ALL: lihat semua data =====
@app.get("/items/")                    # GET ke /items/ (tanpa nomor ID)
def read_all_items():
    return {"items": list(items_db.values())}  # values() = ambil semua isi dictionary, list() = ubah jadi daftar

# ===== 8. READ ONE: lihat satu data =====
@app.get("/items/{item_id}")           # {item_id} = bagian alamat yang berubah-ubah (path parameter)
def read_item(item_id: int):           # nilai dari alamat; ": int" memastikan harus angka bulat
    if item_id not in items_db:        # cek: apakah ID itu tidak ada di penyimpanan?
        raise HTTPException(status_code=404, detail="Item not found")  # hentikan fungsi, kirim error 404
    return {"item": items_db[item_id]} # kalau lolos pengecekan, ID pasti ada, kirim datanya

# ===== 9. UPDATE: ubah data =====
@app.put("/items/{item_id}")           # PUT ke /items/3 misalnya
def update_item(item_id: int, item: Item):  # item_id dari alamat, item (data baru) dari isi permintaan
    if item_id not in items_db:        # pastikan data yang mau diubah memang ada
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id].update(item.model_dump(exclude_unset=True))
    # exclude_unset=True = hanya ambil field yang BENAR-BENAR dikirim klien
    # update()           = timpa nilai lama dengan nilai baru, field lain dibiarkan
    # contoh: kirim {"ipk": 3.9} -> hanya ipk yang berubah
    return {"message": f"Item with ID: {item_id} updated", "item": items_db[item_id]}

# ===== 10. DELETE: hapus data =====
@app.delete("/items/{item_id}")        # DELETE ke /items/3 misalnya
def delete_item(item_id: int):
    if item_id not in items_db:        # pastikan data yang mau dihapus ada
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id)  # pop() = hapus dari dictionary SEKALIGUS mengembalikan isinya
    return {"message": f"Item with ID: {item_id} deleted", "item": deleted_item}  # tampilkan data yang baru dihapus