import psycopg2
from postgres_tutorial import config


def write_blob(part_id, path_to_file, file_extension):
    """ insert a BLOB into a table """

    conn = None
    try:
        # read data from a picture
        drawing = open(path_to_file, 'rb').read()

        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute("INSERT INTO part_drawings(part_id, file_extension,"
                    "drawing_data) VALUES (%s, %s, %s)",
                    (part_id, file_extension, psycopg2.Binary(drawing)))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def read_blob(part_id, path_to_dir):
    """ read BLOB data from a table """

    conn = None
    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(""" SELECT part_name, file_extension, drawing_data
                                FROM part_drawings
                                INNER JOIN parts on parts.part_id = part_drawings.part_id
                                WHERE parts.part_id = %s """,
                    (part_id,))

        blob = cur.fetchone()
        open(path_to_dir + blob[0] + '.' + blob[1], 'wb').write(blob[2])
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    # write_blob(1, 'images/pips.jpg', 'jpg')
    # write_blob(2, 'images/glazz.jpg', 'jpg')

    read_blob(1, 'images/blob/')
    # read_blob(2, 'images/blob/')
