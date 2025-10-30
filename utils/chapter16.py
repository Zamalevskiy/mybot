# utils/chapter16.py

users_reached_ch16 = set()

def mark_user_reached_chapter_16(user_id: int):
    users_reached_ch16.add(user_id)

def user_reached_chapter_16(user_id: int) -> bool:
    return user_id in users_reached_ch16
