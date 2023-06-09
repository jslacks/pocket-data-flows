const name = 'DataFlows';
const domainPrefix = 'data-flows';
const s3BucketPrefix = 'impact';
const isDev = process.env.NODE_ENV === 'development';
const environment = isDev ? 'Dev' : 'Prod';
const fullEnvironment = isDev ? 'development' : 'production';
const domain = isDev
  ? `${domainPrefix}.impactsystems.net`
  : `${domainPrefix}.impactsystems.net`;
const graphqlVariant = isDev ? 'development' : 'current';
const githubConnectionArn = isDev
  ? 'arn:aws:codestar-connections:us-west-2:480076400879:connection/32316762-9d08-4734-95d4-7043b1119270'
  : 'arn:aws:codestar-connections:us-west-2:480076400879:connection/32316762-9d08-4734-95d4-7043b1119270';
const branch = isDev ? 'dev' : 'main';

// Git branch name is used to determine which Prefect project to register the tasks in: dev or prod.
// In the future we might support feature deployments where the project is created automatically during deployment.
const prefectProjectName = branch;
const prefect = {
  api: 'https://api.prefect.io', // Use Prefect Cloud
  port: 8080, // Port for health check server
  projectName: prefectProjectName,
  agentContainerName: 'app',
  agentLabels: [prefectProjectName],
  agentLevel: isDev ? 'DEBUG' : 'INFO',
  // The flowTask object below configures the ECS tasks that execute the Prefect flows.
  flowTask: {
    // See the documentation below for valid values for CPU and memory:
    // https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html#cfn-ecs-taskdefinition-cpu
    cpu: 4096,
    memory: 30720,
    // For queuing large files to disk... https://docs.amazonaws.cn/en_us/AmazonECS/latest/userguide/fargate-task-defs.html#fargate-tasks-storage
    ephemeralStorageSizeInGB: 200,
    dataLearningBucketName: isDev
      ? 'impact-virtuoso-maestro'
      : 'impact-virtuoso-maestro',


    // To securely inject an environment variable FOO_BAR in the ECS task that executes Prefect Flows, add 'FOO_BAR' to
    // the list below and create Parameters /DataFlows/Prod/FOO_BAR and /DataFlows/Dev/FOO_BAR in Prod and Dev.
    parameterStoreNames: ['FOO_BAR'],



    // Use the existing 'PocketDataProductReadOnly' policy. It currently only exists in production.
    // @see https://github.com/Pocket/data-shared/blob/main/lib/permissions-stack.ts#L14
    existingPolicies: isDev ? [] : ['PocketDataProductWriteAccess'],
  },
};

export const config = {
  name,
  isDev,
  prefix: `${name}-${environment}`,
  awsRegion: 'us-west-2',
  s3BucketPrefix,
  circleCIPrefix: `/${name}/CircleCI/${environment}`,
  shortName: 'DATAFL',
  environment,
  fullEnvironment,
  domain,
  prefect,
  terraform: {
    organization: 'impact-analytics',
  },
  codePipeline: {
    artifactBucketPrefix: `${s3BucketPrefix}-codepipeline`,
    githubConnectionArn,
    repository: 'jslacks/pocket-data-flows',
    branch,
    codeDeploySnsTopicName: `DataFlows-${environment}-Notify`,
  },
  graphqlVariant,
  healthCheck: {
    command: [
      'CMD-SHELL',
      // Prefect exposes a simple health check: https://docs.prefect.io/orchestration/agents/overview.html#health-checks
      // The Prefect Docker image (based on python:3.9-slim) does not have curl or wget installed, so we'll use Python
      // to make a request to the health check endpoint.
      `python -c 'import requests; requests.get("http://localhost:${prefect.port}/api/health").raise_for_status()' || exit 1`,
    ],
    interval: 15,
    retries: 3,
    timeout: 5,
    startPeriod: 0,
  },
  tags: {
    service: name,
    environment,
  },
};
