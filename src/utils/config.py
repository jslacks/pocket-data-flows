import base64
import os

ENV_LOCAL = "local"
ENV_DEV = "development"
ENV_PROD = "production"
PROJECT_LOCAL = "local"

ENVIRONMENT = os.getenv("ENVIRONMENT", ENV_LOCAL)

PREFECT_PROJECT_NAME = os.getenv("PREFECT_PROJECT_NAME", PROJECT_LOCAL)
PREFECT_S3_RESULT_BUCKET = os.getenv("PREFECT_S3_RESULT_BUCKET")

GCS_BUCKET = (
    "pocket-prefect-stage-prod"
    if ENVIRONMENT == ENV_PROD
    else "pocket-prefect-stage-dev"
)
GCS_PATH_DEFAULT = ENVIRONMENT
GCS_PATH = os.getenv("GCS_PATH", GCS_PATH_DEFAULT)

SNOWFLAKE_DEV_SCHEMA_DEFAULT = "DEV_DATA_ENGINEERING"
SNOWFLAKE_DEV_SCHEMA = os.getenv("SNOWFLAKE_DEV_SCHEMA", SNOWFLAKE_DEV_SCHEMA_DEFAULT)
SNOWFLAKE_STAGE = (
    "prefect.public.prefect_gcs_stage_parq_prod"
    if ENVIRONMENT == ENV_PROD
    else "development.public.prefect_gcs_stage_parq_dev"
)
SNOWFLAKE_DB = "prefect" if ENVIRONMENT == ENV_PROD else "development"
SNOWFLAKE_MOZILLA_SCHEMA = (
    "mozilla" if ENVIRONMENT == ENV_PROD else SNOWFLAKE_DEV_SCHEMA
)
SNOWFLAKE_ANALYTICS_DATABASE = "ANALYTICS"
SNOWFLAKE_ANALYTICS_DBT_STAGING_SCHEMA = os.getenv(
    "SNOWFLAKE_ANALYTICS_DBT_STAGING_SCHEMA",
    "DBT_STAGING",  # For local development, set the Dbt staging schema in .env
)
SNOWFLAKE_ANALYTICS_DBT_SCHEMA = os.getenv("SNOWFLAKE_ANALYTICS_DBT_SCHEMA", "DBT")

BRAZE_API_KEY = os.getenv("BRAZE_API_KEY")
BRAZE_REST_ENDPOINT = os.getenv("BRAZE_REST_ENDPOINT")

_BASE64_SNOWFLAKE_PRIVATE_KEY = os.getenv("SNOWFLAKE_PRIVATE_KEY")

SNOWFLAKE_DEFAULT_DICT = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "private_key": base64.b64decode(_BASE64_SNOWFLAKE_PRIVATE_KEY)
    if _BASE64_SNOWFLAKE_PRIVATE_KEY
    else None,
}

SNOWFLAKE_DATA_RETENTION_CONNECTION_DICT = {
    **SNOWFLAKE_DEFAULT_DICT,
    "warehouse": os.getenv("SNOWFLAKE_DATA_RETENTION_WAREHOUSE"),
    "role": os.getenv("SNOWFLAKE_DATA_RETENTION_ROLE"),
    "database": os.getenv("SNOWFLAKE_DATA_RETENTION_DB"),
    "schema": os.getenv("SNOWFLAKE_DATA_RETENTION_SCHEMA"),
}

_MYSQL_PUBLISHER_PORT = os.getenv("POCKET_PUBLISHER_DATABASE_PORT")
MYSQL_PUBLISHER_CONNECTION_DICT = {
    "host": os.getenv("POCKET_PUBLISHER_DATABASE_HOST"),
    "user": os.getenv("POCKET_PUBLISHER_DATABASE_USER"),
    "db_name": os.getenv("POCKET_PUBLISHER_DATABASE_DBNAME"),
    "port": int(_MYSQL_PUBLISHER_PORT) if _MYSQL_PUBLISHER_PORT else 3306,
    "password": os.getenv("POCKET_PUBLISHER_DATABASE_PASSWORD"),
}

SNOWFLAKE_SNOWPLOW_DB = os.getenv("SNOWFLAKE_SNOWPLOW_DB")
SNOWFLAKE_SNOWPLOW_SCHEMA = os.getenv("SNOWFLAKE_SNOWPLOW_SCHEMA")
SNOWFLAKE_RAWDATA_DB = os.getenv("SNOWFLAKE_RAWDATA_DB")
SNOWFLAKE_RAWDATA_FIREHOSE_SCHEMA = os.getenv("SNOWFLAKE_RAWDATA_FIREHOSE_SCHEMA")
SNOWFLAKE_SNAPSHOT_DB = os.getenv("SNOWFLAKE_SNAPSHOT_DB")
SNOWFLAKE_SNAPSHOT_FIREHOSE_SCHEMA = os.getenv("SNOWFLAKE_SNAPSHOT_FIREHOSE_SCHEMA")

ATHENA_S3_OUTPUT = os.getenv("PREFECT_S3_ATHENA_QUERY_OUTPUT_BUCKET")


SQS_MESSAGE_VERSION = 3
SQS_REC_QUEUE = (
    "RecommendationAPI-Prod-Sqs-Translation-Queue"
    if ENVIRONMENT == ENV_PROD
    else "RecommendationAPI-Dev-Sqs-Translation-Queue"
)
SQS_PROSPECT_QUEUE = (
    "ProspectAPI-Prod-Sqs-Translation-Queue"
    if ENVIRONMENT == ENV_PROD
    else "ProspectAPI-Dev-Sqs-Translation-Queue"
)


ARTICLES_DB_SCHEMA_DICT = {
    "local": {
        "articles_database_name": os.getenv("SNOWFLAKE_DB"),
        "articles_schema_name": os.getenv("SNOWFLAKE_DEV_SCHEMA"),
    },
    "production": {
        "articles_database_name": "raw",
        "articles_schema_name": "item",
    },
}
