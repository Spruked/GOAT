-- GOAT Database Initialization
-- Courtroom-Grade AI Evidence Preparation System

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS goat;
CREATE SCHEMA IF NOT EXISTS audit;

-- Set search path
SET search_path TO goat, public;

-- Create custom types
CREATE TYPE evidence_status AS ENUM ('pending', 'processing', 'certified', 'minted', 'archived', 'rejected');
CREATE TYPE authority_level AS ENUM ('human', 'ai', 'system');
CREATE TYPE integration_type AS ENUM ('apex_doc', 'truemark', 'external');

-- Create evidence bundles table
CREATE TABLE IF NOT EXISTS evidence_bundles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bundle_id VARCHAR(255) UNIQUE NOT NULL,
    case_id VARCHAR(255),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status evidence_status DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(255) NOT NULL,
    authority_level authority_level NOT NULL,
    metadata JSONB DEFAULT '{}',
    hash_sha256 VARCHAR(64) NOT NULL,
    signature TEXT,
    encryption_key_hash VARCHAR(64),
    file_path VARCHAR(1000),
    file_size BIGINT,
    mime_type VARCHAR(255)
);

-- Create integrations table
CREATE TABLE IF NOT EXISTS integrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    integration_type integration_type NOT NULL,
    endpoint_url VARCHAR(1000) NOT NULL,
    api_key_hash VARCHAR(64),
    public_key TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_health_check TIMESTAMP WITH TIME ZONE,
    health_status VARCHAR(50) DEFAULT 'unknown',
    config JSONB DEFAULT '{}'
);

-- Create audit log table
CREATE TABLE IF NOT EXISTS audit.audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id VARCHAR(255),
    action VARCHAR(255) NOT NULL,
    resource_type VARCHAR(255) NOT NULL,
    resource_id VARCHAR(255),
    details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    authority_level authority_level,
    success BOOLEAN DEFAULT true,
    error_message TEXT
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_evidence_bundles_status ON evidence_bundles(status);
CREATE INDEX IF NOT EXISTS idx_evidence_bundles_created_at ON evidence_bundles(created_at);
CREATE INDEX IF NOT EXISTS idx_evidence_bundles_case_id ON evidence_bundles(case_id);
CREATE INDEX IF NOT EXISTS idx_evidence_bundles_bundle_id ON evidence_bundles(bundle_id);
CREATE INDEX IF NOT EXISTS idx_integrations_type ON integrations(integration_type);
CREATE INDEX IF NOT EXISTS idx_integrations_status ON integrations(status);
CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit.audit_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit.audit_log(action);
CREATE INDEX IF NOT EXISTS idx_audit_log_resource ON audit.audit_log(resource_type, resource_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers
CREATE TRIGGER update_evidence_bundles_updated_at
    BEFORE UPDATE ON evidence_bundles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_integrations_updated_at
    BEFORE UPDATE ON integrations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create audit trigger function
CREATE OR REPLACE FUNCTION audit.audit_trigger_function()
RETURNS TRIGGER AS $$
DECLARE
    action_type TEXT;
    old_data JSONB;
    new_data JSONB;
BEGIN
    -- Determine action type
    IF TG_OP = 'INSERT' THEN
        action_type := 'INSERT';
        old_data := NULL;
        new_data := row_to_json(NEW)::JSONB;
    ELSIF TG_OP = 'UPDATE' THEN
        action_type := 'UPDATE';
        old_data := row_to_json(OLD)::JSONB;
        new_data := row_to_json(NEW)::JSONB;
    ELSIF TG_OP = 'DELETE' THEN
        action_type := 'DELETE';
        old_data := row_to_json(OLD)::JSONB;
        new_data := NULL;
    END IF;

    -- Insert audit record
    INSERT INTO audit.audit_log (
        user_id,
        action,
        resource_type,
        resource_id,
        details,
        success
    ) VALUES (
        COALESCE(current_setting('app.user_id', true), 'system'),
        action_type,
        TG_TABLE_NAME,
        CASE
            WHEN TG_OP = 'DELETE' THEN (old_data->>'id')
            ELSE (new_data->>'id')
        END,
        jsonb_build_object(
            'old_data', old_data,
            'new_data', new_data,
            'table_name', TG_TABLE_NAME,
            'operation', TG_OP
        ),
        true
    );

    RETURN CASE
        WHEN TG_OP = 'DELETE' THEN OLD
        ELSE NEW
    END;
END;
$$ LANGUAGE plpgsql;

-- Create audit triggers (optional - enable as needed)
-- CREATE TRIGGER audit_evidence_bundles
--     AFTER INSERT OR UPDATE OR DELETE ON evidence_bundles
--     FOR EACH ROW EXECUTE FUNCTION audit.audit_trigger_function();

-- Insert default integration records
INSERT INTO integrations (integration_type, endpoint_url, status)
VALUES
    ('apex_doc', 'https://api.apex-doc.com/v1', 'inactive'),
    ('truemark', 'https://api.truemark.com/v1', 'inactive')
ON CONFLICT DO NOTHING;

-- Create views for monitoring
CREATE OR REPLACE VIEW goat.evidence_stats AS
SELECT
    status,
    COUNT(*) as count,
    MIN(created_at) as oldest,
    MAX(created_at) as newest
FROM evidence_bundles
GROUP BY status;

CREATE OR REPLACE VIEW goat.system_health AS
SELECT
    integration_type,
    status,
    health_status,
    last_health_check,
    EXTRACT(EPOCH FROM (NOW() - last_health_check)) / 60 as minutes_since_check
FROM integrations
WHERE status = 'active';

-- Grant permissions
GRANT USAGE ON SCHEMA goat TO goat;
GRANT USAGE ON SCHEMA audit TO goat;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA goat TO goat;
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA audit TO goat;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA goat TO goat;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA audit TO goat;

-- Create goat user if not exists (this will be handled by environment variables)
-- The password should be set via POSTGRES_PASSWORD environment variable