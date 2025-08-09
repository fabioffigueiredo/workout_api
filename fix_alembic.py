
import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(user='workout', password='workout',
                                 database='workout', host='localhost')
    try:
        await conn.execute('DELETE FROM alembic_version')
        print("Tabela alembic_version limpa com sucesso.")
    except asyncpg.exceptions.UndefinedTableError:
        print("Tabela alembic_version não encontrada. Nenhuma ação necessária.")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
