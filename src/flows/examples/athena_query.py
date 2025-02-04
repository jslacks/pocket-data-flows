import prefect
from prefect import Flow, task

from api_clients.athena import athena_query
from utils.config import ENVIRONMENT, ENV_PROD
from utils.flow import get_flow_name

FLOW_NAME = get_flow_name(__file__)

ATHENA_DATABASE = 'production-user-recommendation-preferences-v1-1654798646' if ENVIRONMENT == ENV_PROD else \
    'development-user-recommendation-preferences-v1-1654826050'

@task()
def log_query_result(result):
    logger = prefect.context.get("logger")
    logger.info(f'Query result: {result}')


with Flow(FLOW_NAME) as flow:
    query_result = athena_query(
        query=f'SELECT COUNT(*) FROM "sagemaker_featurestore"."{ATHENA_DATABASE}"',
    )

    log_query_result(query_result)

if __name__ == "__main__":
    flow.run()
