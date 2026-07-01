CREATE TABLE pipeline_runs (

    id SERIAL PRIMARY KEY,

    pipeline_name VARCHAR(100),

    status VARCHAR(50),

    start_time TIMESTAMP,

    end_time TIMESTAMP,

    duration_seconds INTEGER,

    records_processed INTEGER,

    error_message TEXT

);