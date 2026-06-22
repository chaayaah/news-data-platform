CREATE TABLE IF NOT EXISTS pipeline_runs (

    id SERIAL PRIMARY KEY,

    pipeline_name VARCHAR(100),

    status VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);