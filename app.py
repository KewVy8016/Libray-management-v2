"""
app.py  —  Entry Point ของระบบบริหารจัดการห้องสมุด
=====================================================
ไฟล์นี้เป็น Streamlit UI หลัก ประกอบด้วย 4 หน้า:
    📚 หน้าแรก  — แสดงรายการหนังสือทั้งหมด + Sort
    ➕ เพิ่มหนังสือ — ฟอร์มกรอกข้อมูล
    ✏️ แก้ไข / ลบ — เลือกและแก้ไข/ลบหนังสือ
    🔍 ค้นหา    — ค้นหาด้วย ISBN หรือชื่อหนังสือ

วิธีรัน:
    streamlit run app.py
"""

import streamlit as st

# Import CRUD Model
from models import Book, BookManager

# Import Algorithms ที่เขียนเอง
from algorithms.sorting import insertion_sort, merge_sort
from algorithms.searching import binary_search, sequential_search

# ===== Page Config =====
st.set_page_config(
    page_title="ระบบบริหารจัดการห้องสมุด",
    page_icon="📚",
    layout="wide",
)

# ===== Session State Initialization =====
# ใช้ st.session_state เก็บ BookManager เพื่อไม่ให้สร้างใหม่ทุก rerun
if "manager" not in st.session_state:
    st.session_state.manager = BookManager()

# ชื่อย่อเพื่อใช้งานสะดวก
manager: BookManager = st.session_state.manager


# ===== Helper: เลือก Sort Algorithm ตาม PRD =====

def smart_sort(books: list, key: str, reverse: bool) -> list:
    """
    เลือก Algorithm ตาม PRD Section 4.2:
        - < 10 เล่ม  → Insertion Sort
        - ≥ 10 เล่ม  → Merge Sort

    Args:
        books   (list): List ของ dict หนังสือ
        key     (str) : Field ที่ใช้เรียง ('year' หรือ 'author')
        reverse (bool): True = มากไปน้อย

    Returns:
        list: List หนังสือที่เรียงแล้ว + ชื่อ algorithm ที่ใช้
    """
    count = len(books)
    if count < 10:
        # ข้อมูลน้อย — ใช้ Insertion Sort
        algo_name = "Insertion Sort"
        sorted_books = insertion_sort(books, key, reverse)
    else:
        # ข้อมูลมาก — ใช้ Merge Sort
        algo_name = "Merge Sort"
        sorted_books = merge_sort(books, key, reverse)

    return sorted_books, algo_name


# ===== Helper: ดึงหนังสือที่เรียง ISBN แล้ว (สำหรับ Binary Search) =====

def get_books_sorted_by_isbn() -> list:
    """
    คืน List หนังสือที่เรียงตาม ISBN แล้ว
    ใช้ merge_sort ตรงๆ เพราะไม่จำกัดจำนวน (Binary Search ต้องการข้อมูลเรียง)
    """
    all_books = manager.get_all()
    if not all_books:
        return []
    # เรียงด้วย merge_sort ทุกครั้งเพื่อความถูกต้องของ Binary Search
    return merge_sort(all_books, "isbn", reverse=False)


# ===================================================
# ==================  SIDEBAR  =====================
# ===================================================

st.sidebar.title("📚 ห้องสมุด")
st.sidebar.markdown("---")

# เมนูนำทาง
page = st.sidebar.radio(
    "เมนู",
    options=["📚 หน้าแรก", "➕ เพิ่มหนังสือ", "✏️ แก้ไข / ลบ", "🔍 ค้นหา"],
    label_visibility="collapsed",
)

# แสดงจำนวนหนังสือในระบบบน Sidebar
st.sidebar.markdown("---")
st.sidebar.metric("หนังสือในระบบ", manager.get_count(), "เล่ม")


# ===================================================
# ============  PAGE 1: หน้าแรก (แสดงทั้งหมด)  ======
# ===================================================

if page == "📚 หน้าแรก":
    st.title("📚 รายการหนังสือทั้งหมด")

    all_books = manager.get_all()

    if not all_books:
        # แสดงข้อความถ้ายังไม่มีหนังสือ
        st.info("ยังไม่มีหนังสือในระบบ — กรุณาเพิ่มหนังสือก่อน")
    else:
        # ─── ตัวเลือก Sort ───
        st.subheader("⚙️ ตัวเลือกการเรียงลำดับ")
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            sort_key = st.selectbox(
                "เรียงตาม",
                options=["year", "author"],
                format_func=lambda x: "ปีที่พิมพ์" if x == "year" else "ชื่อผู้แต่ง",
                key="home_sort_key",
            )

        with col2:
            sort_direction = st.selectbox(
                "ทิศทาง",
                options=["asc", "desc"],
                format_func=lambda x: "น้อยไปมาก ↑" if x == "asc" else "มากไปน้อย ↓",
                key="home_sort_dir",
            )

        with col3:
            st.write("")  # spacer
            st.write("")  # spacer
            do_sort = st.button("🔀 เรียงลำดับ", key="btn_sort_home", use_container_width=True)

        # เรียงและแสดงผล
        reverse = sort_direction == "desc"
        sorted_books, algo_used = smart_sort(all_books, sort_key, reverse)

        st.markdown("---")

        # แสดง Algorithm ที่ใช้ (ตาม Success Criteria ข้อ 2 ของ PRD)
        key_label = "ปีที่พิมพ์" if sort_key == "year" else "ชื่อผู้แต่ง"
        dir_label = "มากไปน้อย" if reverse else "น้อยไปมาก"
        st.caption(f"🔧 Algorithm: **{algo_used}** | เรียงตาม: **{key_label}** ({dir_label})")

        # เพิ่มเลขลำดับก่อนแสดง
        display_data = []
        for idx, book in enumerate(sorted_books, start=1):
            row = {"#": idx}
            row.update(book)
            display_data.append(row)

        # แสดงใน dataframe ตาม PRD Section 4.4
        st.dataframe(display_data, use_container_width=True)
        st.caption(f"📖 จำนวนหนังสือทั้งหมด: **{len(sorted_books)} เล่ม**")


# ===================================================
# ============  PAGE 2: เพิ่มหนังสือ  ===============
# ===================================================

elif page == "➕ เพิ่มหนังสือ":
    st.title("➕ เพิ่มหนังสือใหม่")
    st.markdown("กรอกข้อมูลให้ครบทุกช่อง (ทุก field จำเป็น)")

    # ─── ฟอร์มกรอกข้อมูล ───
    with st.form("add_book_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            # ISBN input
            isbn = st.text_input(
                "ISBN *",
                placeholder="เช่น 978-616-1234-56-7",
                help="รหัส ISBN ต้องไม่ซ้ำกันในระบบ",
            )
            # ชื่อหนังสือ
            title = st.text_input(
                "ชื่อหนังสือ *",
                placeholder="เช่น Python เบื้องต้น",
            )
            # ชื่อผู้แต่ง
            author = st.text_input(
                "ชื่อผู้แต่ง *",
                placeholder="เช่น สมชาย ใจดี",
            )

        with col2:
            # ปีที่พิมพ์
            year = st.number_input(
                "ปีที่พิมพ์ (ค.ศ.) *",
                min_value=1,
                max_value=2100,
                value=2024,
                step=1,
            )
            # สำนักพิมพ์
            publisher = st.text_input(
                "สำนักพิมพ์ *",
                placeholder="เช่น ซีเอ็ด",
            )
            # หมวดหมู่
            category = st.text_input(
                "หมวดหมู่ *",
                placeholder="เช่น เทคโนโลยี",
            )

        # ปุ่ม Submit
        submitted = st.form_submit_button("💾 บันทึก", use_container_width=True)

    # ─── ประมวลผลหลัง Submit ───
    if submitted:
        new_book = Book(isbn, title, author, int(year), publisher, category)
        success, message = manager.add_book(new_book)

        if success:
            st.success(f"✅ {message}")
        else:
            st.error(f"❌ {message}")


# ===================================================
# ============  PAGE 3: แก้ไข / ลบ  ================
# ===================================================

elif page == "✏️ แก้ไข / ลบ":
    st.title("✏️ แก้ไข / ลบ หนังสือ")

    all_books = manager.get_all()

    if not all_books:
        st.info("ยังไม่มีหนังสือในระบบ")
    else:
        # Dropdown เลือกหนังสือ — แสดงในรูปแบบ "ชื่อ (ISBN)"
        # ใช้ Sequential Search ดึงข้อมูลมาแสดงใน form ตาม PRD Section 4.1 Update
        book_options = {
            f"{b['title']} ({b['isbn']})": b["isbn"] for b in all_books
        }

        selected_label = st.selectbox(
            "เลือกหนังสือ",
            options=list(book_options.keys()),
            key="edit_select",
        )
        selected_isbn = book_options[selected_label]

        # Sequential Search หา dict ของหนังสือที่เลือก
        selected_book = None
        for b in all_books:
            if b["isbn"] == selected_isbn:
                selected_book = b
                break

        if selected_book:
            st.markdown("---")

            # ─── แท็บแก้ไข / ลบ ───
            tab_edit, tab_delete = st.tabs(["✏️ แก้ไข", "🗑️ ลบ"])

            # ── แท็บแก้ไข ──
            with tab_edit:
                st.subheader(f"แก้ไข: {selected_book['title']}")

                with st.form("edit_book_form"):
                    col1, col2 = st.columns(2)

                    with col1:
                        # ISBN แสดงอย่างเดียว (ห้ามแก้ไขตาม PRD)
                        st.text_input(
                            "ISBN (ไม่สามารถเปลี่ยนได้)",
                            value=selected_book["isbn"],
                            disabled=True,
                        )
                        new_title = st.text_input(
                            "ชื่อหนังสือ *",
                            value=selected_book["title"],
                        )
                        new_author = st.text_input(
                            "ชื่อผู้แต่ง *",
                            value=selected_book["author"],
                        )

                    with col2:
                        new_year = st.number_input(
                            "ปีที่พิมพ์ (ค.ศ.) *",
                            min_value=1,
                            max_value=2100,
                            value=selected_book["year"],
                            step=1,
                        )
                        new_publisher = st.text_input(
                            "สำนักพิมพ์ *",
                            value=selected_book["publisher"],
                        )
                        new_category = st.text_input(
                            "หมวดหมู่ *",
                            value=selected_book["category"],
                        )

                    save_btn = st.form_submit_button("💾 บันทึกการแก้ไข", use_container_width=True)

                if save_btn:
                    success, message = manager.update_book(
                        isbn=selected_isbn,
                        title=new_title,
                        author=new_author,
                        year=int(new_year),
                        publisher=new_publisher,
                        category=new_category,
                    )
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()  # รีโหลดหน้าเพื่อแสดงข้อมูลใหม่
                    else:
                        st.error(f"❌ {message}")

            # ── แท็บลบ ──
            with tab_delete:
                st.subheader(f"ลบ: {selected_book['title']}")
                st.warning(
                    f"⚠️ คุณกำลังจะลบหนังสือ **'{selected_book['title']}'** "
                    f"(ISBN: {selected_book['isbn']}) — การดำเนินการนี้ไม่สามารถยกเลิกได้"
                )

                # Confirmation checkbox ก่อนลบ (ทำหน้าที่เป็น Confirmation dialog ตาม PRD)
                confirm = st.checkbox(
                    "ฉันยืนยันว่าต้องการลบหนังสือเล่มนี้",
                    key="confirm_delete",
                )

                # ปุ่มลบ — ใช้งานได้เมื่อกด Confirm เท่านั้น
                if st.button(
                    "🗑️ ยืนยันการลบ",
                    disabled=not confirm,
                    use_container_width=True,
                    type="primary",
                ):
                    success, message = manager.delete_book(selected_isbn)
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()  # รีโหลดหน้าหลังลบ
                    else:
                        st.error(f"❌ {message}")


# ===================================================
# ============  PAGE 4: ค้นหา  =====================
# ===================================================

elif page == "🔍 ค้นหา":
    st.title("🔍 ค้นหาหนังสือ")

    # เลือกประเภทการค้นหา
    search_type = st.radio(
        "ประเภทการค้นหา",
        options=["ISBN (Binary Search)", "ชื่อหนังสือ (Sequential Search)"],
        horizontal=True,
    )

    st.markdown("---")

    # ─── Binary Search ด้วย ISBN ───
    if search_type == "ISBN (Binary Search)":
        st.subheader("🔍 ค้นหาด้วย ISBN")
        st.caption("Algorithm: **Binary Search** | ต้องการ List ที่เรียง ISBN ก่อน")

        isbn_query = st.text_input(
            "กรอก ISBN ที่ต้องการค้นหา",
            placeholder="เช่น 978-616-1234-56-7",
            key="isbn_search_input",
        )

        if st.button("🔍 ค้นหา", key="btn_isbn_search"):
            if not isbn_query.strip():
                st.warning("กรุณากรอก ISBN ก่อนค้นหา")
            else:
                # ดึง List ที่เรียง ISBN แล้วสำหรับ Binary Search
                sorted_by_isbn = get_books_sorted_by_isbn()

                # Binary Search — O(log n)
                result = binary_search(sorted_by_isbn, isbn_query.strip())

                if result:
                    st.success(f"✅ พบ 1 รายการ")
                    st.dataframe([result], use_container_width=True)
                else:
                    st.error(f"❌ ไม่พบ ISBN '{isbn_query}' ในระบบ")

    # ─── Sequential Search ด้วยชื่อ ───
    else:
        st.subheader("🔍 ค้นหาด้วยชื่อหนังสือ")
        st.caption("Algorithm: **Sequential Search** | รองรับการค้นหาแบบ Partial match")

        title_query = st.text_input(
            "กรอกชื่อหนังสือ (บางส่วนก็ได้)",
            placeholder="เช่น Python",
            key="title_search_input",
        )

        if st.button("🔍 ค้นหา", key="btn_title_search"):
            if not title_query.strip():
                st.warning("กรุณากรอกคำค้นหาก่อน")
            else:
                all_books = manager.get_all()

                # Sequential Search — O(n), ไม่ต้องเรียงก่อน
                results = sequential_search(all_books, title_query.strip())

                if results:
                    st.success(f"✅ พบ {len(results)} รายการ")
                    st.dataframe(results, use_container_width=True)
                else:
                    st.info(f"ℹ️ ไม่พบหนังสือที่มีชื่อตรงกับ '{title_query}'")
