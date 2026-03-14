"""
models.py  —  Data Model และ CRUD Operations
=============================================
ไฟล์นี้ดูแล:
    - Class Book       : โครงสร้างข้อมูลหนังสือหนึ่งเล่ม
    - Class BookManager: จัดการ List ของหนังสือทั้งหมด
                         รวมถึง CRUD + Persist ด้วย JSON
"""

import json
import os

# ===== Constants =====
# กำหนด Path ของไฟล์ข้อมูล relative กับไฟล์นี้
_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(_DATA_DIR, "books.json")


# ===== Data Model =====

class Book:
    """
    แทนหนังสือ 1 เล่มในระบบ

    Attributes:
        isbn      (str): รหัส ISBN — Unique, ห้ามซ้ำ
        title     (str): ชื่อหนังสือ
        author    (str): ชื่อผู้แต่ง
        year      (int): ปีที่พิมพ์ (ค.ศ.)
        publisher (str): สำนักพิมพ์
        category  (str): หมวดหมู่ เช่น "เทคโนโลยี"
    """

    def __init__(
        self,
        isbn: str,
        title: str,
        author: str,
        year: int,
        publisher: str,
        category: str,
    ):
        self.isbn = isbn.strip()
        self.title = title.strip()
        self.author = author.strip()
        self.year = int(year)
        self.publisher = publisher.strip()
        self.category = category.strip()

    def to_dict(self) -> dict:
        """แปลง Book object เป็น dictionary (ใช้เก็บใน List และ JSON)"""
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "publisher": self.publisher,
            "category": self.category,
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        """สร้าง Book object จาก dictionary (ใช้ตอนโหลดจาก JSON)"""
        return Book(
            isbn=data["isbn"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            publisher=data["publisher"],
            category=data["category"],
        )

    def __repr__(self) -> str:
        return f"Book(isbn={self.isbn!r}, title={self.title!r})"


# ===== Book Manager (CRUD on List) =====

class BookManager:
    """
    จัดการ List ของหนังสือทั้งหมด

    ใช้ Python List เป็น Data Structure หลัก
    บันทึก/โหลดข้อมูลผ่านไฟล์ JSON เพื่อให้ข้อมูลคงอยู่ (Persist)
    """

    def __init__(self):
        # _books เป็น List หลักที่เก็บ dict ของหนังสือทุกเล่ม
        self._books: list[dict] = []
        self._load_from_file()  # โหลดข้อมูลจากไฟล์เมื่อสร้าง instance

    # ── Persistence (โหลด / บันทึก JSON) ──────────────────────────────────

    def _load_from_file(self) -> None:
        """
        โหลดข้อมูลหนังสือจาก books.json
        ถ้าไฟล์ยังไม่มี จะสร้างไฟล์เปล่าให้อัตโนมัติ
        """
        # สร้าง directory ถ้ายังไม่มี
        os.makedirs(_DATA_DIR, exist_ok=True)

        if not os.path.exists(DATA_FILE):
            # ไฟล์ยังไม่มี → เริ่มด้วย List ว่างและสร้างไฟล์
            self._books = []
            self._save_to_file()
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self._books = json.load(f)  # โหลด JSON → Python List[dict]
        except (json.JSONDecodeError, IOError):
            # ถ้าไฟล์เสียหาย เริ่มต้นใหม่ด้วย List ว่าง
            self._books = []

    def _save_to_file(self) -> None:
        """
        บันทึก List หนังสือปัจจุบันลง books.json
        เรียกหลัง Add / Update / Delete ทุกครั้ง
        """
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            # indent=2 ทำให้ JSON อ่านง่าย, ensure_ascii=False รองรับภาษาไทย
            json.dump(self._books, f, ensure_ascii=False, indent=2)

    # ── Read ───────────────────────────────────────────────────────────────

    def get_all(self) -> list[dict]:
        """คืนค่า copy ของ List หนังสือทั้งหมด (เพื่อป้องกัน external mutation)"""
        return self._books[:]

    def get_count(self) -> int:
        """คืนจำนวนหนังสือในระบบ"""
        return len(self._books)

    def isbn_exists(self, isbn: str) -> bool:
        """
        ตรวจสอบว่า ISBN นี้มีอยู่ในระบบแล้วหรือไม่
        ใช้วนลูปตรงๆ เพราะยังไม่มีข้อกำหนดว่าต้อง sort ก่อน
        """
        for book in self._books:
            if book["isbn"] == isbn.strip():
                return True
        return False

    # ── Create ─────────────────────────────────────────────────────────────

    def add_book(self, book: Book) -> tuple[bool, str]:
        """
        เพิ่มหนังสือใหม่เข้า List

        Validation:
            - ทุก field ต้องไม่ว่าง
            - ISBN ต้องไม่ซ้ำกับที่มีอยู่

        Args:
            book (Book): หนังสือที่ต้องการเพิ่ม

        Returns:
            tuple[bool, str]: (สำเร็จ, ข้อความแจ้ง)
        """
        # ตรวจสอบว่าทุก field ไม่ว่าง
        ok, msg = _validate_book(book)
        if not ok:
            return False, msg

        # ตรวจสอบ ISBN ซ้ำ
        if self.isbn_exists(book.isbn):
            return False, f"ISBN '{book.isbn}' มีอยู่ในระบบแล้ว"

        # Append เข้า List หลัก
        self._books.append(book.to_dict())
        self._save_to_file()  # บันทึกทันที
        return True, f"เพิ่มหนังสือ '{book.title}' สำเร็จ"

    # ── Update ─────────────────────────────────────────────────────────────

    def update_book(
        self,
        isbn: str,
        title: str,
        author: str,
        year: int,
        publisher: str,
        category: str,
    ) -> tuple[bool, str]:
        """
        แก้ไขข้อมูลหนังสือโดยค้นหาจาก ISBN (ISBN เปลี่ยนไม่ได้)

        ใช้ Sequential Search หาตำแหน่งหนังสือใน List
        แล้ว Update ค่าใหม่ใน dict โดยตรง

        Args:
            isbn      (str): ISBN ของหนังสือที่ต้องการแก้ไข
            title ... (str): ข้อมูลใหม่

        Returns:
            tuple[bool, str]: (สำเร็จ, ข้อความแจ้ง)
        """
        # ตรวจสอบ field ว่างก่อน
        dummy = Book(isbn, title, author, year, publisher, category)
        ok, msg = _validate_book(dummy)
        if not ok:
            return False, msg

        # Sequential Search หาหนังสือที่ต้องการ
        for book in self._books:
            if book["isbn"] == isbn.strip():
                # พบแล้ว → อัปเดตค่าใหม่
                book["title"] = title.strip()
                book["author"] = author.strip()
                book["year"] = int(year)
                book["publisher"] = publisher.strip()
                book["category"] = category.strip()
                self._save_to_file()  # บันทึกทันที
                return True, f"แก้ไขหนังสือ '{title}' สำเร็จ"

        return False, f"ไม่พบ ISBN '{isbn}' ในระบบ"

    # ── Delete ─────────────────────────────────────────────────────────────

    def delete_book(self, isbn: str) -> tuple[bool, str]:
        """
        ลบหนังสือออกจาก List โดยค้นหาจาก ISBN

        หา index ของหนังสือก่อน แล้วใช้ list.pop() เพื่อลบ

        Args:
            isbn (str): ISBN ของหนังสือที่ต้องการลบ

        Returns:
            tuple[bool, str]: (สำเร็จ, ข้อความแจ้ง)
        """
        # หา index ของหนังสือที่ต้องการลบ
        target_index = -1
        for i, book in enumerate(self._books):
            if book["isbn"] == isbn.strip():
                target_index = i
                break

        if target_index == -1:
            return False, f"ไม่พบ ISBN '{isbn}' ในระบบ"

        # ลบออกจาก List ด้วย pop()
        removed = self._books.pop(target_index)
        self._save_to_file()  # บันทึกทันที
        return True, f"ลบหนังสือ '{removed['title']}' สำเร็จ"


# ===== Helper Functions =====

def _validate_book(book: Book) -> tuple[bool, str]:
    """
    ตรวจสอบความถูกต้องของข้อมูล Book ก่อน Add/Update

    Rules:
        - ทุก field ต้องไม่ว่าง (ไม่อนุญาต whitespace-only)
        - year ต้องเป็นตัวเลขและมีค่า > 0

    Returns:
        tuple[bool, str]: (ผ่าน, ข้อความ error หรือ "")
    """
    if not book.isbn:
        return False, "กรุณากรอก ISBN"
    if not book.title:
        return False, "กรุณากรอกชื่อหนังสือ"
    if not book.author:
        return False, "กรุณากรอกชื่อผู้แต่ง"
    if not book.publisher:
        return False, "กรุณากรอกสำนักพิมพ์"
    if not book.category:
        return False, "กรุณากรอกหมวดหมู่"
    if book.year <= 0:
        return False, "ปีที่พิมพ์ต้องมากกว่า 0"
    return True, ""
