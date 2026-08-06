from database import get_connection


# =====================================================
# LOGIN & USER MANAGEMENT
# =====================================================

def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT *
        FROM users
        WHERE username=%s AND password=%s
        """
        cursor.execute(query, (username, password))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def register_user(username, password, nama, foto_profil=""):
    """Menambahkan user baru ke database"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Cek apakah username sudah ada
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, "Username sudah digunakan!"

        # Simpan user baru
        sql = "INSERT INTO users (username, password, nama, foto) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (username, password, nama, foto_profil))
        conn.commit()
        return True, "Berhasil"
    except Exception as e:
        conn.rollback()
        return False, f"Database Error: {e}"
    finally:
        cursor.close()
        conn.close()


def get_user_profile(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT id, nama, username, foto FROM users WHERE id=%s"
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def update_profile(user_id, nama, username, password, foto):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if password:
            query = """
            UPDATE users
            SET nama=%s, username=%s, password=%s, foto=%s
            WHERE id=%s
            """
            cursor.execute(query, (nama, username, password, foto, user_id))
        else:
            query = """
            UPDATE users
            SET nama=%s, username=%s, foto=%s
            WHERE id=%s
            """
            cursor.execute(query, (nama, username, foto, user_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


# =====================================================
# PROJECT
# =====================================================

def get_projects(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT
            projects.id,
            projects.kode_proyek,
            projects.nama_proyek,
            clients.nama_client,
            projects.status
        FROM projects
        JOIN clients ON projects.client_id = clients.id
        WHERE projects.user_id = %s
        ORDER BY projects.id DESC
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_project_detail(project_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT
            projects.id,
            projects.kode_proyek,
            projects.nama_proyek,
            clients.nama_client,
            projects.status
        FROM projects
        JOIN clients ON projects.client_id = clients.id
        WHERE projects.id=%s
        """
        cursor.execute(query, (project_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def add_project(user_id, nama_proyek, nama_client="-"):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if not nama_client:
            nama_client = "-"

        # CEK CLIENT
        cursor.execute("SELECT id FROM clients WHERE nama_client=%s", (nama_client,))
        client = cursor.fetchone()

        if client:
            client_id = client["id"]
        else:
            cursor.execute("INSERT INTO clients (nama_client) VALUES(%s)", (nama_client,))
            client_id = cursor.lastrowid

        # GENERATE KODE PROJECT
        cursor.execute("SELECT kode_proyek FROM projects ORDER BY id DESC LIMIT 1")
        last = cursor.fetchone()

        if last:
            nomor = int(last["kode_proyek"].replace("PRJ", "")) + 1
        else:
            nomor = 1

        kode = f"PRJ{nomor:03d}"

        # INSERT PROJECT DENGAN USER_ID
        cursor.execute(
            """
            INSERT INTO projects (user_id, client_id, kode_proyek, nama_proyek, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, client_id, kode, nama_proyek, "Aktif")
        )
        conn.commit()
        return kode
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def update_project(project_id, nama_proyek, nama_client):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM clients WHERE nama_client=%s", (nama_client,))
        client = cursor.fetchone()

        if client:
            client_id = client["id"]
        else:
            cursor.execute("INSERT INTO clients (nama_client) VALUES(%s)", (nama_client,))
            client_id = cursor.lastrowid

        cursor.execute(
            """
            UPDATE projects
            SET nama_proyek=%s, client_id=%s
            WHERE id=%s
            """,
            (nama_proyek, client_id, project_id)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM transactions WHERE project_id=%s", (project_id,))
        cursor.execute("DELETE FROM projects WHERE id=%s", (project_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


# =====================================================
# CLIENT
# =====================================================

def get_clients():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM clients ORDER BY nama_client ASC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_client_by_name(nama_client):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM clients WHERE nama_client=%s", (nama_client,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def add_client(nama_client):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clients (nama_client) VALUES(%s)", (nama_client,))
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()


# =====================================================
# TRANSACTION
# =====================================================

def get_transactions(project_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT id, tanggal, kategori, keterangan, jenis, nominal, nota
        FROM transactions
        WHERE project_id=%s
        ORDER BY tanggal,
        FIELD(kategori, 'Saldo Awal', 'Saldo Masuk', 'Material', 'Tenaga', 'Alat Kerja', 'Operasional', 'Prive'), id
        """
        cursor.execute(query, (project_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def add_transaction(project_id, tanggal, kategori, keterangan, jenis, nominal, nota):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO transactions (project_id, tanggal, kategori, keterangan, jenis, nominal, nota)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (project_id, tanggal, kategori, keterangan, jenis, nominal, nota))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_transaction_by_id(transaction_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM transactions WHERE id=%s", (transaction_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def update_transaction(transaction_id, tanggal, keterangan, jenis, nominal, kategori=None, nota=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if kategori is not None and nota is not None:
            query = """
            UPDATE transactions
            SET tanggal=%s, kategori=%s, keterangan=%s, jenis=%s, nominal=%s, nota=%s
            WHERE id=%s
            """
            cursor.execute(query, (tanggal, kategori, keterangan, jenis, nominal, nota, transaction_id))
        else:
            query = """
            UPDATE transactions
            SET tanggal=%s, keterangan=%s, jenis=%s, nominal=%s
            WHERE id=%s
            """
            cursor.execute(query, (tanggal, keterangan, jenis, nominal, transaction_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM transactions WHERE id=%s", (transaction_id,))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()


def get_transaction_summary(project_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT
            SUM(CASE WHEN jenis='Pemasukan' THEN nominal ELSE 0 END) AS pemasukan,
            SUM(CASE WHEN jenis='Pengeluaran' THEN nominal ELSE 0 END) AS pengeluaran
        FROM transactions
        WHERE project_id=%s
        """
        cursor.execute(query, (project_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_transactions_by_date(project_id, tanggal_awal, tanggal_akhir):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT id, tanggal, kategori, keterangan, jenis, nominal, nota
        FROM transactions
        WHERE project_id=%s AND tanggal BETWEEN %s AND %s
        ORDER BY tanggal,
        FIELD(kategori, 'Saldo Awal', 'Saldo Masuk', 'Material', 'Tenaga', 'Alat Kerja', 'Operasional', 'Prive'), id
        """
        cursor.execute(query, (project_id, tanggal_awal, tanggal_akhir))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


# =====================================================
# DASHBOARD STATISTICS & GRAPH (PER USER)
# =====================================================

def get_dashboard_summary(user_id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if user_id is not None:
            cursor.execute("SELECT COUNT(*) AS total FROM projects WHERE user_id = %s", (user_id,))
            total_project = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT SUM(t.nominal) AS total 
                FROM transactions t 
                JOIN projects p ON t.project_id = p.id 
                WHERE p.user_id = %s AND t.jenis = 'Pemasukan'
            """, (user_id,))
            income = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT SUM(t.nominal) AS total 
                FROM transactions t 
                JOIN projects p ON t.project_id = p.id 
                WHERE p.user_id = %s AND t.jenis = 'Pengeluaran'
            """, (user_id,))
            expense = cursor.fetchone()["total"]
        else:
            cursor.execute("SELECT COUNT(*) AS total FROM projects")
            total_project = cursor.fetchone()["total"]

            cursor.execute("SELECT SUM(nominal) AS total FROM transactions WHERE jenis='Pemasukan'")
            income = cursor.fetchone()["total"]

            cursor.execute("SELECT SUM(nominal) AS total FROM transactions WHERE jenis='Pengeluaran'")
            expense = cursor.fetchone()["total"]

        return {
            "project": total_project or 0,
            "income": income or 0,
            "expense": expense or 0,
            "balance": (income or 0) - (expense or 0)
        }
    finally:
        cursor.close()
        conn.close()


def get_cashflow_chart(user_id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if user_id is not None:
            query = """
            SELECT
                DATE_FORMAT(t.tanggal, '%Y-%m') AS bulan,
                t.jenis,
                SUM(t.nominal) AS total
            FROM transactions t
            JOIN projects p ON t.project_id = p.id
            WHERE p.user_id = %s
            GROUP BY bulan, t.jenis
            ORDER BY bulan ASC
            """
            cursor.execute(query, (user_id,))
        else:
            query = """
            SELECT
                DATE_FORMAT(tanggal,'%Y-%m') AS bulan,
                jenis,
                SUM(nominal) AS total
            FROM transactions
            GROUP BY bulan, jenis
            ORDER BY bulan ASC
            """
            cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()