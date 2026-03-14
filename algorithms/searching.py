"""
searching.py  —  Searching Algorithms สำหรับระบบห้องสมุด
=========================================================
ไฟล์นี้มี 2 Algorithm ที่เขียนเองทั้งหมด (ห้ามใช้ list.index() หรือ filter()):

    1. binary_search()      — ค้นหา ISBN (ต้องการ List ที่เรียง ISBN แล้ว)
    2. sequential_search()  — ค้นหาชื่อหนังสือแบบ Partial match
"""


def binary_search(books: list, isbn: str) -> dict | None:
    """
    Binary Search — ค้นหาหนังสือจาก ISBN

    หลักการทำงาน:
        กำหนดขอบเขต [low, high] แล้วดูที่จุดกลาง (mid)
        - ถ้า ISBN ที่ mid == target  → พบแล้ว return
        - ถ้า ISBN ที่ mid < target   → target อยู่ครึ่งขวา เลื่อน low
        - ถ้า ISBN ที่ mid > target   → target อยู่ครึ่งซ้าย เลื่อน high
        ทำซ้ำจนพบหรือ low > high (ไม่พบ)

    ⚠️ ข้อกำหนด: books ต้องถูกเรียงตาม isbn ก่อนเสมอ ไม่เช่นนั้นผลลัพธ์จะไม่ถูกต้อง

    เวลา: O(log n)

    Args:
        books (list): List ของ dict หนังสือที่เรียงตาม isbn แล้ว
        isbn  (str) : ISBN ที่ต้องการค้นหา

    Returns:
        dict | None: dict หนังสือที่พบ หรือ None ถ้าไม่พบ
    """
    low = 0               # ขอบซ้ายของช่วงการค้นหา
    high = len(books) - 1  # ขอบขวาของช่วงการค้นหา

    while low <= high:
        # หาจุดกลาง (ใช้ integer division)
        mid = (low + high) // 2
        mid_isbn = books[mid]["isbn"]

        if mid_isbn == isbn:
            # พบ ISBN ที่ต้องการ
            return books[mid]
        elif mid_isbn < isbn:
            # ISBN ที่ mid น้อยกว่า target → ค้นหาในครึ่งขวา
            low = mid + 1
        else:
            # ISBN ที่ mid มากกว่า target → ค้นหาในครึ่งซ้าย
            high = mid - 1

    # ไม่พบ ISBN ในระบบ
    return None


def sequential_search(books: list, query: str) -> list:
    """
    Sequential Search — ค้นหาหนังสือจากชื่อแบบ Partial match

    หลักการทำงาน:
        วนลูปตรวจสอบทุก element ใน List
        นำชื่อหนังสือและคำค้นหามาแปลงเป็นตัวพิมพ์เล็กก่อนเปรียบเทียบ
        เพื่อให้ Case-insensitive และรองรับ Partial match

    ⚠️ ข้อกำหนด: ห้ามใช้ list.index() หรือ filter()

    เวลา: O(n)

    Args:
        books (list): List ของ dict หนังสือ (ไม่ต้องเรียงลำดับก่อน)
        query (str) : คำที่ต้องการค้นหา (รองรับบางส่วน)

    Returns:
        list: List ของ dict หนังสือที่ชื่อมีคำค้นหาอยู่
    """
    results = []                 # เก็บผลลัพธ์ที่ค้นพบ
    query_lower = query.lower()  # แปลงคำค้นเป็นพิมพ์เล็กสำหรับ case-insensitive

    # วนลูปตรวจสอบทุกเล่มในระบบ (Sequential = ทีละตัวตามลำดับ)
    for book in books:
        title_lower = book["title"].lower()  # แปลงชื่อหนังสือเป็นพิมพ์เล็ก

        # ตรวจสอบว่าคำค้นอยู่ในชื่อหนังสือหรือไม่ (Partial match)
        if query_lower in title_lower:
            results.append(book)  # เพิ่มลงผลลัพธ์ถ้าตรงกัน

    return results
