import datetime
import sqlite3

DB_NAME = "myproject.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    """데이터베이스 및 테이블 자동 생성"""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. users 테이블 생성
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # 2. learning_history 테이블 생성
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS learning_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT NOT NULL,
            m1 INTEGER, m2 INTEGER, m3 INTEGER, m4 INTEGER, m5 INTEGER,
            m6 INTEGER, m7 INTEGER, m8 INTEGER, m9 INTEGER, m10 INTEGER,
            score INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (userid) REFERENCES users(userid)
        )
    """
    )

    conn.commit()
    conn.close()


def register_user(userid, password):
    """신규 회원 가입"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (userid, password) VALUES (?, ?)",
            (userid, password),
        )
        conn.commit()
        return True, "회원가입이 성공적으로 완료되었습니다."
    except sqlite3.IntegrityError:
        return False, "이미 존재하는 아이디입니다."
    finally:
        conn.close()


def login_user(userid, password):
    """로그인 검증"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE userid = ? AND password = ?",
        (userid, password),
    )
    user = cursor.fetchone()
    conn.close()
    return user


def save_quiz_result(userid, user_answers, score):
    """형성평가 응시 결과 저장 (m1~m10 정답 번호, 총점, 응시 일시)"""
    conn = get_connection()
    cursor = conn.cursor()

    # m1 ~ m10 길이 보장 (10개 요소)
    answers = user_answers + [None] * (10 - len(user_answers))

    query = """
        INSERT INTO learning_history (userid, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, [userid] + answers + [score])
    conn.commit()
    conn.close()


def get_user_history(userid):
    """특정 사용자의 형성평가 응시 기록 조회 (최신순)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, score, created_at
        FROM learning_history
        WHERE userid = ?
        ORDER BY created_at DESC
    """,
        (userid,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows