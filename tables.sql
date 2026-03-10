CREATE TABLE mmwave_sensor_data (
    id BIGSERIAL PRIMARY KEY,
    created_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL, -- 自動帶入包含時區的當下時間
    breath_rate NUMERIC(5, 2), 
    heart_rate NUMERIC(5, 2),  
    breath_phase NUMERIC(5, 2), 
    heart_phase NUMERIC(5, 2), 
    status_code INTEGER NOT NULL -- 預設為NOT NULL
);


CREATE TABLE environment_sensor_data (
    id BIGSERIAL PRIMARY KEY,
    created_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    temperature NUMERIC(5, 2), 
    humidity NUMERIC(5, 2),    
    light_level NUMERIC(5, 2)
);


CREATE TABLE agent (
    alert_id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    trigger_source VARCHAR(50) NOT NULL, 
    action_taken TEXT,                  
    resolved BOOLEAN DEFAULT FALSE NOT NULL -- 預設為FALSE
);
