"""Conexão e operações (CRUD) no banco Oracle."""
import os
import getpass
import oracledb


def conectar():
    """Conecta ao Oracle usando variáveis de ambiente ou pedindo no prompt."""
    usuario = os.getenv("ORACLE_USER") or input("Usuário Oracle: ").strip()
    senha = os.getenv("ORACLE_PASSWORD") or getpass.getpass("Senha Oracle: ")
    dsn = os.getenv("ORACLE_DSN", "oracle.fiap.com.br:1521/ORCL")
    return oracledb.connect(user=usuario, password=senha, dsn=dsn)


def criar_tabela(conn):
    """Cria a tabela caso ainda não exista."""
    ddl = """
    CREATE TABLE COLHEITA_CANA (
        ID            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        TALHAO        VARCHAR2(50)  NOT NULL,
        SAFRA         VARCHAR2(7)   NOT NULL,
        AREA_HA       NUMBER(10,2)  NOT NULL,
        PRODUTIVIDADE NUMBER(10,2)  NOT NULL,
        TIPO_COLHEITA VARCHAR2(10)  NOT NULL CHECK (TIPO_COLHEITA IN ('MANUAL','MECANICA')),
        PERDA_PCT     NUMBER(5,2)   NOT NULL,
        PERDA_TON     NUMBER(12,2)  NOT NULL,
        PERDA_RS      NUMBER(14,2)  NOT NULL,
        STATUS        VARCHAR2(10)  NOT NULL,
        DT_REGISTRO   DATE DEFAULT SYSDATE
    )"""
    with conn.cursor() as cur:
        try:
            cur.execute(ddl)
        except oracledb.DatabaseError as e:
            if "ORA-00955" not in str(e):  # tabela já existe
                raise


def inserir(conn, reg):
    sql = """INSERT INTO COLHEITA_CANA
             (TALHAO, SAFRA, AREA_HA, PRODUTIVIDADE, TIPO_COLHEITA,
              PERDA_PCT, PERDA_TON, PERDA_RS, STATUS)
             VALUES (:talhao, :safra, :area_ha, :produtividade, :tipo,
                     :perda_pct, :perda_ton, :perda_rs, :status)"""
    with conn.cursor() as cur:
        cur.execute(sql, reg)
    conn.commit()


def listar(conn):
    """Retorna lista de dicionários com todos os registros."""
    sql = """SELECT ID, TALHAO, SAFRA, AREA_HA, PRODUTIVIDADE, TIPO_COLHEITA,
                    PERDA_PCT, PERDA_TON, PERDA_RS, STATUS
             FROM COLHEITA_CANA ORDER BY ID"""
    chaves = ("id", "talhao", "safra", "area_ha", "produtividade", "tipo",
              "perda_pct", "perda_ton", "perda_rs", "status")
    with conn.cursor() as cur:
        cur.execute(sql)
        return [dict(zip(chaves, linha)) for linha in cur.fetchall()]


def atualizar(conn, id_reg, perda_pct, perda_ton, perda_rs, status):
    sql = """UPDATE COLHEITA_CANA SET PERDA_PCT=:p, PERDA_TON=:t, PERDA_RS=:r, STATUS=:s
             WHERE ID=:id"""
    with conn.cursor() as cur:
        cur.execute(sql, {"p": perda_pct, "t": perda_ton, "r": perda_rs,
                          "s": status, "id": id_reg})
        afetadas = cur.rowcount
    conn.commit()
    return afetadas


def remover(conn, id_reg):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM COLHEITA_CANA WHERE ID=:id", {"id": id_reg})
        afetadas = cur.rowcount
    conn.commit()
    return afetadas
