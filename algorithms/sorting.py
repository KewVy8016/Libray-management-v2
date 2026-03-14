"""
sorting.py  —  Sorting Algorithms สำหรับระบบห้องสมุด
===================================================
ไฟล์นี้มี 2 Algorithm ที่เขียนเองทั้งหมด (ห้ามใช้ sorted() / sort()):

    1. insertion_sort()  — ใช้เมื่อจำนวนหนังสือน้อยกว่า 10 เล่ม
    2. merge_sort()      — ใช้เมื่อจำนวนหนังสือตั้งแต่ 10 เล่มขึ้นไป

ทั้งสอง Algorithm รับ List ของ dictionary (หนังสือ) และ
คืนค่าเป็น List ใหม่ที่เรียงลำดับแล้ว (ไม่แก้ List เดิม)
"""


def insertion_sort(books: list, key: str, reverse: bool = False) -> list:
    """
    Insertion Sort — เรียงลำดับแบบแทรก

    หลักการทำงาน:
        วนจากซ้ายไปขวา สำหรับแต่ละ element ให้นำมา "แทรก"
        ลงในตำแหน่งที่ถูกต้องในส่วนที่เรียงแล้วทางซ้าย
        เปรียบเหมือนการเรียงไพ่ในมือ

    เวลา: O(n²) — เหมาะสำหรับ n น้อย (< 10)

    Args:
        books   (list): List ของ dict หนังสือ
        key     (str) : Field ที่ใช้เรียง เช่น 'year' หรือ 'author'
        reverse (bool): True = มากไปน้อย, False = น้อยไปมาก

    Returns:
        list: List ของหนังสือที่เรียงแล้ว (copy ใหม่)
    """
    # สร้าง copy เพื่อไม่แก้ไข List ต้นฉบับ
    arr = books[:]

    # วนจาก index 1 ถึงท้าย List (index 0 ถือว่า "เรียงแล้ว" อยู่แล้ว)
    for i in range(1, len(arr)):
        # นำ element ปัจจุบันมาเป็น "key element" ที่จะหาตำแหน่งแทรก
        current = arr[i]
        current_val = current[key]

        # ตำแหน่งของ element ก่อนหน้า
        j = i - 1

        # เลื่อน element ที่มากกว่า current ไปทางขวา
        # เพื่อเปิดช่องว่างสำหรับ current
        while j >= 0:
            compare_val = arr[j][key]

            if not reverse:
                # เรียงน้อยไปมาก: ถ้า element ซ้ายมากกว่า ก็เลื่อนออก
                should_shift = compare_val > current_val
            else:
                # เรียงมากไปน้อย: ถ้า element ซ้ายน้อยกว่า ก็เลื่อนออก
                should_shift = compare_val < current_val

            if should_shift:
                arr[j + 1] = arr[j]  # เลื่อน element ไปขวาหนึ่งช่อง
                j -= 1
            else:
                break  # เจอตำแหน่งที่ถูกต้องแล้ว หยุดได้

        # วาง current ลงในตำแหน่งที่หาได้
        arr[j + 1] = current

    return arr


def merge_sort(books: list, key: str, reverse: bool = False) -> list:
    """
    Merge Sort — เรียงลำดับแบบแบ่งแล้วรวม (Divide and Conquer)

    หลักการทำงาน:
        แบ่ง List ออกเป็นสองครึ่ง (Divide)
        เรียงแต่ละครึ่งแบบ Recursive
        แล้วรวม (Merge) สองครึ่งที่เรียงแล้วเข้าด้วยกัน

    เวลา: O(n log n) — เหมาะสำหรับ n มาก (≥ 10)

    Args:
        books   (list): List ของ dict หนังสือ
        key     (str) : Field ที่ใช้เรียง เช่น 'year' หรือ 'author'
        reverse (bool): True = มากไปน้อย, False = น้อยไปมาก

    Returns:
        list: List ของหนังสือที่เรียงแล้ว (copy ใหม่)
    """
    # Base case: ถ้า List มี 0 หรือ 1 element ถือว่าเรียงแล้ว
    if len(books) <= 1:
        return books[:]

    # --- Divide: หาจุดกึ่งกลางแล้วแบ่ง ---
    mid = len(books) // 2
    left_half = books[:mid]   # ครึ่งซ้าย
    right_half = books[mid:]  # ครึ่งขวา

    # --- Conquer: เรียงแต่ละครึ่งแบบ Recursive ---
    sorted_left = merge_sort(left_half, key, reverse)
    sorted_right = merge_sort(right_half, key, reverse)

    # --- Merge: รวมสองครึ่งที่เรียงแล้ว ---
    return _merge(sorted_left, sorted_right, key, reverse)


def _merge(left: list, right: list, key: str, reverse: bool) -> list:
    """
    ฟังก์ชันภายใน: รวม List สองชุดที่เรียงแล้วให้เป็น List เดียว

    Args:
        left    (list): List ซ้ายที่เรียงแล้ว
        right   (list): List ขวาที่เรียงแล้ว
        key     (str) : Field ที่ใช้เปรียบเทียบ
        reverse (bool): ทิศทางการเรียง

    Returns:
        list: List ที่รวมและเรียงแล้ว
    """
    result = []   # List ผลลัพธ์
    i = 0         # pointer ของ left
    j = 0         # pointer ของ right

    # เปรียบเทียบทีละคู่จาก left และ right แล้วนำตัวที่ควรมาก่อนใส่ result
    while i < len(left) and j < len(right):
        left_val = left[i][key]
        right_val = right[j][key]

        if not reverse:
            # เรียงน้อยไปมาก: ถ้า left น้อยกว่าหรือเท่ากัน นำ left มาก่อน
            take_left = left_val <= right_val
        else:
            # เรียงมากไปน้อย: ถ้า left มากกว่าหรือเท่ากัน นำ left มาก่อน
            take_left = left_val >= right_val

        if take_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # นำ element ที่เหลือของ left (ถ้ามี) ต่อท้าย
    result.extend(left[i:])

    # นำ element ที่เหลือของ right (ถ้ามี) ต่อท้าย
    result.extend(right[j:])

    return result
