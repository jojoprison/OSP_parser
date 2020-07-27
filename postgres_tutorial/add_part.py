import psycopg2
from postgres_tutorial import config


def add_part(part_name, vendor_list):
    insert_part = "INSERT INTO parts(part_name) VALUES(%s) RETURNING part_id;"
    assign_vendor = "INSERT INTO vendor_parts(vendor_id, part_id) VALUES (%s, %s)"

    conn = None
    try:
        params = config.config()

        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute(insert_part, (part_name,))

                part_id = cur.fetchone()[0]

                for vendor_id in vendor_list:
                    cur.execute(assign_vendor, (vendor_id, part_id))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    # add_part('SIM Tray', (13, 14))
    # add_part('Speaker', (15, 16))
    # add_part('Vibrator', (17, 18))
    # add_part('Antenna', (18, 19))
    # add_part('Home Button', (13, 17))
    # add_part('LTE Modem', (13, 17))

    add_part('Power Amplifier', (19,))
