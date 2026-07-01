import psycopg2


def get_connection():

    return psycopg2.connect(
        host="news-postgres",
        database="newsdb",
        user="postgres",
        password="postgres"
    )


def start_pipeline(pipeline_name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO pipeline_runs
        (
            pipeline_name,
            status,
            start_time
        )
        VALUES
        (
            %s,
            %s,
            NOW()
        )
        RETURNING id
        """,
        (
            pipeline_name,
            "RUNNING"
        )
    )

    pipeline_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return pipeline_id


def finish_pipeline(
    pipeline_id,
    duration,
    records_processed
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE pipeline_runs
        SET
            status=%s,
            end_time=NOW(),
            duration_seconds=%s,
            records_processed=%s
        WHERE id=%s
        """,
        (
            "SUCCESS",
            duration,
            records_processed,
            pipeline_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()


def fail_pipeline(
    pipeline_id,
    duration,
    error_message
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE pipeline_runs
        SET
            status=%s,
            end_time=NOW(),
            duration_seconds=%s,
            error_message=%s
        WHERE id=%s
        """,
        (
            "FAILED",
            duration,
            error_message,
            pipeline_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()