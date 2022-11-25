import sqlite3
import os

from lib import global_variable as glv


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def conect_db(self):
        db_path = os.path.join(
            glv.get_variable("APP_PATH"),
            "SPDB.db"
        )
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.conn.close()

    def struct_db(self):
        self.conect_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_clientes (
                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(80) NOT NULL,
                email VARCHAR(120),
                cp VARCHAR(20),
                profissao VARCHAR(40),
                nascimento VARCHAR(11),
                datacad VARCHAR(11),
                fiscal char(255),
                lead VARCHAR(50),
                fiel INTEGER
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_enderecos (
                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_cod INTEGER,
                cep VARCHAR(10) NOT NULL,
                cid TEXT,
                endereco VARCHAR(120)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_contatos (
                linha INTEGER PRIMARY KEY,
                tipo VARCHAR(10),
                cliente_cod INTEGER
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_produtos (
                cod INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                servico TEXT NOT NULL,
                material TEXT,
                kg REAL,
                m REAL,
                m2 REAL,
                unit REAL,
                descricao TEXT
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_comercial (
                cod INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                cliente_cod INTEGER,
                cep_cod INTEGER NOT NULL,
                linha INTEGER,
                pagamento TEXT,
                parcelas INTEGER,
                subtotal REAL,
                discount REAL,
                data TEXT,
                total REAL,
                obs TEXT,
                hist TEXT,
                status TEXT,
                tipo TEXT,
                link TEXT,
                pagas INTEGER
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS info (
                cod INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                empresa TEXT,
                titulo TEXT,
                cnpj TEXT,
                ie TEXT,
                pix TEXT,
                banco TEXT,
                conta TEXT,
                agencia TEXT,
                email TEXT,
                ctt TEXT,
                end TEXT,
                loc TEXT,
                cep TEXT
            );
        """)
        self.cursor.execute("SELECT count(*) FROM INFO")
        COUNT = self.cursor.fetchone()[0]
        if COUNT > 0:
            pass
        else:
            create = ""
            self.cursor.execute(" INSERT INTO info (empresa, titulo, cnpj, ie, pix, banco, conta, agencia, email, ctt, end, loc, cep) "
                                "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (create, create, create, create, create, create, create, create, create, create, create, create, create,))
        self.conn.commit()
        self.disconnect_db()
