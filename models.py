"""
models.py

Contains ALL database operations.

No Telegram code should exist here.
"""

from datetime import datetime

from database import get_connection


###############################################################################
# MEMBERS
###############################################################################

def add_member(chat_id, name: str) -> bool:
    """
    Adds a member.

    Returns:
        True if successful
        False if duplicate name
    """

    try:
        with get_connection() as conn:

            conn.execute(
                """
                INSERT INTO members(chat_id, name)
                VALUES(?, ?)
                """,
                (chat_id, name.strip())
            )

            conn.commit()

            return True

    except Exception:
        return False


def delete_member(chat_id, name: str) -> bool:
    """
    Deletes a member.

    Returns False if:
        - member does not exist
        - member has existing sales
    """

    try:
        with get_connection() as conn:

            cursor = conn.execute(
                """
                DELETE FROM members
                WHERE chat_id = ? AND name = ?
                """,
                (chat_id, name.strip())
            )

            conn.commit()

            return cursor.rowcount > 0

    except Exception:
        return False


def get_members(chat_id) -> list[dict]:
    """
    Returns every member.

    Example

    [
        {
            "id":1,
            "name":"Charlie"
        }
    ]
    """

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT *
            FROM members
            WHERE chat_id = ?
            ORDER BY name
            """,
            (chat_id,)
        ).fetchall()

        return [dict(row) for row in rows]


def get_member(member_id: int):

    with get_connection() as conn:

        row = conn.execute(
            """
            SELECT *
            FROM members
            WHERE id=?
            """,
            (member_id,)
        ).fetchone()

        if row is None:
            return None

        return dict(row)


###############################################################################
# SALES
###############################################################################

def create_sale(chat_id: int, payee_member_id: int, sale_price: float, sale_datetime, items):

    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO sales(chat_id, payee_member_id, sale_price, sale_datetime)
            VALUES (?, ?, ?, ?)
            """,
            (chat_id, payee_member_id, sale_price, sale_datetime.isoformat())
        )

        sale_id = cur.lastrowid

        for member_id, qty in items:
            conn.execute(
                """
                INSERT INTO sale_items(sale_id, member_id, quantity)
                VALUES (?, ?, ?)
                """,
                (sale_id, member_id, qty)
            )

        conn.commit()

        return sale_id


def delete_sale(sale_id: int) -> bool:

    with get_connection() as conn:

        cursor = conn.execute(
            """
            DELETE FROM sales
            WHERE id=?
            """,
            (sale_id,)
        )

        conn.commit()

        return cursor.rowcount > 0


def get_sales(chat_id) -> list[dict]:
    """
    Returns all sales.
    """

    with get_connection() as conn:

        rows = conn.execute( 
            """
            SELECT
                s.*,
                m.name AS payee_name
            FROM sales s
            JOIN members m
                ON s.payee_member_id = m.id
            WHERE s.chat_id=?
            ORDER BY s.sale_datetime;
            """,
            (chat_id,)
        ).fetchall()

        return [dict(row) for row in rows]
    
def get_sales_count(chat_id) -> int:

    with get_connection() as conn:

        row = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM sales
            WHERE chat_id=?
            """,
            (chat_id,)
        ).fetchone()

        return row["count"]

def get_all_sale_items(chat_id: int) -> list[dict]:

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT *
            FROM sale_items si
            JOIN sales s ON si.sale_id = s.id
            WHERE s.chat_id = ?
            """,
            (chat_id,)
        ).fetchall()

        return [dict(row) for row in rows]

###############################################################################
# CLEAR SALES
###############################################################################

def clear_all_sales(chat_id):

    with get_connection() as conn:

        conn.execute(
            """
            DELETE FROM sales
            WHERE chat_id=?
            """,
            (chat_id,)
        )

        conn.commit()


def clear_sales_by_date(chat_id, date_string: str):
    """
    date_string

    2026-06-26
    """

    with get_connection() as conn:

        conn.execute(
            """
            DELETE FROM sales
            WHERE DATE(sale_datetime)=? AND chat_id=?
            """,
            (date_string, chat_id)
        )

        conn.commit()
