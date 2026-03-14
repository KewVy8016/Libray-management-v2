# 📚 Product Requirements Document
## ระบบบริหารจัดการห้องสมุด (Library Management System)

| Field | Detail |
|-------|--------|
| Version | 1.0.0 |
| สถานะ | Draft |
| วันที่ | มีนาคม 2026 |
| ประเภท | งานโครงงานวิชาเรียน |

---

## 1. ภาพรวมโครงการ (Project Overview)

ระบบบริหารจัดการห้องสมุด เป็นแอปพลิเคชันที่พัฒนาด้วย **Python** มีหน้าแสดงผลผ่าน **Streamlit** เพื่อให้ผู้ใช้สามารถจัดการข้อมูลหนังสือได้อย่างสะดวก ครอบคลุมการเพิ่ม แก้ไข ลบ ค้นหา และเรียงลำดับข้อมูล โดยใช้ Algorithm พื้นฐานที่เขียนเองทั้งหมด

### 1.1 วัตถุประสงค์

- ฝึกทักษะการใช้ Data Structure (Array/List) ในการเก็บข้อมูล
- เรียนรู้และนำ Sorting Algorithm (Insertion Sort, Merge Sort) ไปใช้งานจริง
- ฝึกการใช้ Searching Algorithm (Binary Search, Sequential Search)
- พัฒนา UI ที่เรียบง่ายและใช้งานได้จริงด้วย Streamlit

### 1.2 กลุ่มเป้าหมาย

- นักศึกษาที่พัฒนาโครงงานวิชา Data Structure / Algorithm
- ผู้ดูแลห้องสมุดขนาดเล็กที่ต้องการระบบจัดการหนังสือพื้นฐาน

---

## 2. ขอบเขตของระบบ (Scope)

| # | ฟีเจอร์ | คำอธิบาย | Algorithm ที่ใช้ |
|---|---------|----------|-----------------|
| 1 | จัดการข้อมูล (CRUD) | เพิ่ม / แก้ไข / ลบ หนังสือ | Python List |
| 2 | เรียงลำดับ (Sort) | เรียงตามปีพิมพ์หรือชื่อผู้แต่ง | Insertion Sort / Merge Sort |
| 3 | ค้นหา ISBN | ค้นหาจากรหัส ISBN | Binary Search |
| 4 | ค้นหาชื่อหนังสือ | ค้นหาจากชื่อหนังสือ | Sequential Search |
| 5 | แสดงรายการ | แสดงหนังสือทั้งหมดในระบบ | — |

---

## 3. ข้อมูลหนังสือ (Data Model)

หนังสือแต่ละเล่มเก็บในรูปแบบ **Python Dictionary** และรวบรวมทั้งหมดใน **List**

| Field | ชื่อภาษาไทย | ประเภทข้อมูล | ตัวอย่าง / หมายเหตุ |
|-------|------------|-------------|---------------------|
| `isbn` | รหัส ISBN | `str` | `"978-616-xxxx-xx-x"` — Unique, ห้ามซ้ำ |
| `title` | ชื่อหนังสือ | `str` | `"Python เบื้องต้น"` |
| `author` | ชื่อผู้แต่ง | `str` | `"สมชาย ใจดี"` |
| `year` | ปีที่พิมพ์ | `int` | `2024` (ค.ศ.) |
| `publisher` | สำนักพิมพ์ | `str` | `"ซีเอ็ด"` |
| `category` | หมวดหมู่ | `str` | `"เทคโนโลยี"`, `"วิทยาศาสตร์"` ฯลฯ |

> ⚠️ ทุก field เป็น **Required** — ไม่อนุญาตให้เว้นว่าง และ `isbn` ต้องไม่ซ้ำกัน

---

## 4. รายละเอียดฟีเจอร์ (Feature Specification)

### 4.1 การจัดการข้อมูล CRUD

#### ➕ เพิ่มหนังสือ (Add)
- ผู้ใช้กรอกข้อมูลผ่านฟอร์มใน Streamlit (`st.text_input`, `st.number_input`)
- ระบบตรวจสอบว่า ISBN ไม่ซ้ำก่อน Append เข้า List
- แสดง Success / Error message ทันที

#### ✏️ แก้ไขหนังสือ (Update)
- ผู้ใช้เลือกหนังสือจาก Dropdown (แสดงชื่อ + ISBN)
- ระบบค้นหาด้วย Sequential Search เพื่อดึงข้อมูลเดิมมาแสดง
- ผู้ใช้แก้ไขข้อมูลที่ต้องการ แล้วกดบันทึก
- `isbn` ไม่อนุญาตให้เปลี่ยนแปลง

#### 🗑️ ลบหนังสือ (Delete)
- ผู้ใช้เลือกหนังสือจาก Dropdown แล้วกดปุ่มลบ
- มี Confirmation dialog ก่อนลบจริง
- ระบบ Remove item ออกจาก List

---

### 4.2 การเรียงลำดับ (Sorting)

> **กฎหลัก:** ใช้ **Insertion Sort** เมื่อจำนวนหนังสือ **< 10 เล่ม** และใช้ **Merge Sort** เมื่อ **≥ 10 เล่ม**

| Algorithm | ใช้เมื่อ | เรียงตามอะไรได้บ้าง | หลักการ |
|-----------|---------|-------------------|---------|
| Insertion Sort | หนังสือ < 10 เล่ม | ปีพิมพ์ / ชื่อผู้แต่ง | วนลูปแทรกทีละตัว เหมาะข้อมูลน้อย |
| Merge Sort | หนังสือ ≥ 10 เล่ม | ปีพิมพ์ / ชื่อผู้แต่ง | แบ่งครึ่งแล้ว Merge เหมาะข้อมูลมาก |

ผู้ใช้สามารถเลือก **Key** (ปีพิมพ์ / ชื่อผู้แต่ง) และ**ทิศทาง** (น้อยไปมาก / มากไปน้อย) ผ่าน UI ก่อนกด Sort

---

### 4.3 การค้นหา (Searching)

| Algorithm | ค้นหาจาก | เงื่อนไขก่อนใช้ | ผลลัพธ์ |
|-----------|---------|----------------|---------|
| Binary Search | ISBN | List ต้องถูก Sort ตาม ISBN ก่อน | พบ 0 หรือ 1 รายการ (ISBN unique) |
| Sequential Search | ชื่อหนังสือ | ไม่ต้องเรียงลำดับ | พบได้หลายรายการ (Partial match) |

ระบบแสดงผลลัพธ์ใน `st.dataframe` พร้อมระบุจำนวนรายการที่พบ

---

### 4.4 แสดงรายการหนังสือทั้งหมด

- แสดงผ่าน `st.dataframe` พร้อมเลขลำดับ
- ระบุให้ชัดเจนว่าเรียงตาม Key และทิศทางใด
- แสดงจำนวนหนังสือทั้งหมด

---

## 5. กฎการใช้ Algorithm (Algorithm Rules)

> ⚠️ **กฎเหล่านี้เป็น Non-negotiable — ห้ามใช้ Built-in `sort()` หรือ Library อื่นแทน**

| หัวข้อ | กฎที่ต้องปฏิบัติ | เหตุผล |
|--------|----------------|--------|
| Insertion Sort | เขียน Logic เองใน `algorithms/sorting.py` ห้ามใช้ `sorted()` | ฝึกทำความเข้าใจ Algorithm |
| Merge Sort | เขียน Recursive merge เองทั้งหมด ห้ามใช้ `sorted()` | ฝึกทำความเข้าใจ Algorithm |
| Binary Search | List ต้อง Sort ตาม ISBN ก่อนเสมอ ห้าม Linear scan | ให้ Algorithm ทำงานถูกต้อง |
| Sequential Search | วนลูป `for` ตรงๆ ห้ามใช้ `list.index()` หรือ `filter()` | ฝึกเขียน Logic เอง |
| Code Style | ทุก Algorithm ต้องมี **Docstring** อธิบายหลักการทำงาน | เพื่อความเข้าใจ |
| Comment | ทุก Step สำคัญต้องมี Comment ภาษาไทยหรืออังกฤษ | อ่านเข้าใจง่าย |

---

## 6. โครงสร้างไฟล์ (File Structure)

```
library-management/
│
├── app.py                  # Entry point — Streamlit UI หลัก
├── models.py               # Class Book + ฟังก์ชัน CRUD บน List
├── requirements.txt        # streamlit (เท่านั้น)
│
├── algorithms/
│   ├── __init__.py
│   ├── sorting.py          # insertion_sort(), merge_sort()
│   └── searching.py        # binary_search(), sequential_search()
│
└── data/
    └── books.json          # ไฟล์เก็บข้อมูลหนังสือ (Persist)
```

| ไฟล์ | หน้าที่ | Dependency |
|------|---------|-----------|
| `app.py` | Streamlit UI หลัก | `models.py`, `algorithms/` |
| `models.py` | Class Book + CRUD บน List | ไม่มี (Pure Python) |
| `algorithms/sorting.py` | `insertion_sort()`, `merge_sort()` | ไม่มี (Pure Python) |
| `algorithms/searching.py` | `binary_search()`, `sequential_search()` | ไม่มี (Pure Python) |
| `data/books.json` | เก็บข้อมูลหนังสือแบบ Persist | `models.py` อ่าน/เขียน |
| `requirements.txt` | รายการ Package | — |

---

## 7. UI/UX Requirements (Streamlit)

### Sidebar Navigation

| เมนู | หน้าที่ |
|------|---------|
| 📚 หน้าแรก | แสดงรายการหนังสือทั้งหมด + ตัวเลือก Sort |
| ➕ เพิ่มหนังสือ | ฟอร์มกรอกข้อมูล |
| ✏️ แก้ไข / ลบ | เลือกหนังสือและดำเนินการ |
| 🔍 ค้นหา | เลือก Search แบบ ISBN หรือ ชื่อหนังสือ |

### หลักการออกแบบ

- **เรียบง่าย ไม่รก** — แต่ละหน้ามีจุดประสงค์เดียว
- **Feedback ทันที** — ทุก Action มี Success / Error message
- **Responsive** — ใช้งานได้บน Desktop Browser

---

## 8. Constraints & Non-Goals

### สิ่งที่ระบบ **ไม่ต้อง** ทำ

- ไม่ต้องทำระบบ Login / Authentication
- ไม่ต้องต่อ Database จริง (ใช้ JSON file พอ)
- ไม่ต้องรองรับ Multi-user พร้อมกัน
- ไม่ต้องทำ Mobile App

### ข้อจำกัดทางเทคนิค

- ใช้ **Python 3.10+** และ **Streamlit** เท่านั้น
- ห้าม Import Library ภายนอกที่เกี่ยวกับ Sort/Search เช่น `numpy.sort`, `pandas.sort`
- Algorithm ทุกตัวต้องเขียนเองทั้งหมด

---

## 9. เกณฑ์ความสำเร็จ (Success Criteria)

| # | เกณฑ์ | วิธีทดสอบ |
|---|-------|----------|
| 1 | CRUD ทำงานครบและข้อมูลไม่สูญหาย | ทดสอบเพิ่ม/แก้ไข/ลบ แล้ว Reload หน้า |
| 2 | Insertion Sort ใช้เมื่อ < 10 เล่ม, Merge Sort ใช้เมื่อ ≥ 10 เล่ม | ตรวจสอบจาก Console / Log |
| 3 | Binary Search หา ISBN ได้ถูกต้อง | ค้นหา ISBN ที่มีและไม่มีในระบบ |
| 4 | Sequential Search ค้นหาชื่อแบบ Partial match ได้ | ค้นหาคำบางส่วนของชื่อหนังสือ |
| 5 | UI ใช้งานได้โดยไม่มี Exception crash | ทดลองใส่ข้อมูลผิดรูปแบบ |

---

*— จบเอกสาร PRD —*
