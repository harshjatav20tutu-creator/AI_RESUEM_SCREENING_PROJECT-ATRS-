SKILL_DATABASE = {
    # Programming Languages
    "python": ["python", "python3"],
    "java": ["java"],
    "c": ["c"],
    "c++": ["c++", "cpp"],
    "c#":  ["c#", "c sharp", "csharp"],
    "javascript": ["javascript", "js"],
    "node.js":["node.js", "node js", "node javascript"],
    "react.js":["react.js","react js","react javascript"],

    # Data & ML
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "data science": ["data science"],
    "artificial intelligence": ["artificial intelligence", "ai","ai ml","aiml"],
    "nlp": ["nlp", "natural language processing"],

    # Libraries / Frameworks
    "numpy": ["numpy"],
    "pandas": ["pandas"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "keras": ["keras"],

    # Databases
    "sql": ["sql", "mysql", "postgresql","relational sql"],
    "nosql":["nosql", " non relational sql", "postgres", "psql"],
    "sql_server": ["sql server", "mssql", "microsoft sql server"],
    "mongodb": ["mongodb", "mongo"],

    # other Tools and CI/CD tools
    "git": ["git", "github"],
    "docker": ["docker"],
    "excel": ["excel", "ms excel"],
    "power bi": ["power bi", "powerbi"],
    "github_actions": ["github actions", "gh actions", "github workflows"],
    "gitlab ci": ["gitlab ci", "gitlab pipelines"],
    "azure devops": ["azure devops", "ado"],
    "kubernetes": ["kubernetes", "k8s"],
    "tableau": ["tableau"],

    # Web / APIs
    "html": ["html"],
    "css": ["css"],
    "flask": ["flask"],
    "fastapi": ["fastapi","fast api"],

    # Cloud (basic)
    "aws": ["aws", "amazon web services"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "azure":["azure","amazon azure"]
}


# 1) STRICT EQUIVALENCE (safe substitutions)
# Use this ONLY when you want: "If JD asks X, Y should count as X".
# Keep this small to avoid wrong matches.
SKILL_EQUIVALENCE = {
    # Cloud platform names (vendor level)
    "aws": ["aws", "amazon web services"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "azure": ["azure", "microsoft azure"],

    # Git (tool) vs GitHub/GitLab (platforms) are NOT equivalent, so keep strict here
    "git": ["git"],

    # Kubernetes common aliases
    "kubernetes": ["kubernetes", "k8s"],

    # CI/CD tool name variants
    "github_actions": ["github actions", "gh actions", "github workflows"],
    "gitlab_ci": ["gitlab ci", "gitlab pipelines"],
    "azure_devops": ["azure devops", "ado"],

    # SQL Server variants
    "sql_server": ["sql server", "mssql", "microsoft sql server"],

    # Postgres variants
    "postgresql": ["postgresql", "postgres", "psql"],

    # JavaScript runtime naming
    "nodejs": ["node", "nodejs", "node js"],

    # React naming variants
    "react": ["react", "reactjs", "react.js", "react js"],
}

# 2) RELATED FAMILIES (NOT equivalent)
# Use this when you want: "Candidate has something close, mark as REVIEW or give partial score".
SKILL_FAMILIES = {
    # Cloud and infra ecosystem
    "cloud_platform": ["aws", "azure", "gcp", "digitalocean", "ibm cloud", "oracle cloud"],
    "cloud_compute": ["ec2", "lambda", "cloud run", "azure functions"],
    "cloud_storage": ["s3", "azure blob storage", "gcs"],
    "cloud_networking": ["vpc", "route53", "cloudfront", "api gateway", "load balancer"],
    "cloud_security": ["iam", "kms", "secrets manager", "key vault"],

    # Databases and data stores
    "relational_database": ["mysql", "postgresql", "sql_server", "oracle db", "mariadb", "sqlite", "amazon aurora"],
    "nosql_database": ["mongodb", "cassandra", "dynamodb", "couchbase", "redis", "neo4j", "firebase firestore"],
    "search_engine": ["elasticsearch", "opensearch", "solr"],
    "data_warehouse": ["snowflake", "amazon redshift", "google bigquery", "azure synapse", "databricks sql"],
    "data_lake": ["delta lake", "iceberg", "hudi"],

    # DevOps / SRE
    "containerization": ["docker", "podman", "docker swarm"],
    "orchestration": ["kubernetes", "helm", "kustomize", "amazon eks", "amazon ecs"],
    "ci_cd": ["jenkins", "github_actions", "gitlab_ci", "circleci", "travis ci", "bamboo", "azure_devops"],
    "infrastructure_as_code": ["terraform", "pulumi", "aws cloudformation", "ansible", "chef", "puppet"],
    "monitoring": ["prometheus", "grafana", "datadog", "new relic", "cloudwatch"],
    "logging": ["elk", "elasticsearch", "logstash", "kibana", "splunk", "loki"],
    "version_control_platform": ["github", "gitlab", "bitbucket"],
    "os_and_scripting": ["linux", "bash", "powershell"],

    # Backend and APIs
    "python_backend": ["django", "flask", "fastapi", "pyramid", "tornado"],
    "node_backend": ["express", "nestjs", "koa", "fastify"],
    "java_backend": ["spring boot", "spring", "quarkus", "micronaut", "hibernate"],
    "api_style": ["rest", "graphql", "grpc"],
    "auth": ["jwt", "oauth", "oauth2", "saml"],

    # Frontend
    "frontend_framework": ["react", "angular", "vue", "svelte", "ember.js", "next.js"],
    "css_framework": ["tailwind", "tailwindcss", "bootstrap", "material ui", "mui", "bulma", "sass", "less"],
    "build_tools": ["webpack", "vite", "babel"],

    # Data engineering and analytics
    "streaming": ["kafka", "kinesis", "pubsub", "rabbitmq"],
    "workflow_orchestration": ["apache airflow", "airflow", "dagster", "prefect"],
    "big_data_processing": ["apache spark", "spark", "hadoop", "apache flink"],
    "etl_tools": ["dbt", "ssis", "informatica", "talend"],
    "data_visualization": ["tableau", "power bi", "looker", "qlikview", "metabase", "superset"],

    # ML / AI (important for our project)
    "ml_frameworks": ["scikit-learn", "sklearn", "tensorflow", "pytorch", "keras", "xgboost", "lightgbm", "catboost"],
    "nlp": ["spacy", "nltk", "transformers", "huggingface", "sentence transformers"],
    "llm_stack": ["openai api", "anthropic", "gemini", "llama", "mistral", "langchain", "llamaindex"],
    "vector_databases": ["faiss", "pinecone", "weaviate", "qdrant", "chroma", "milvus"],
    "mlops": ["mlflow", "wandb", "kubeflow", "sagemaker", "vertex ai", "azure ml"],
    "deployment": ["docker", "kubernetes", "fastapi", "bentoML", "ray serve"],

    # Testing and quality
    "testing_python": ["pytest", "unittest", "nose"],
    "testing_js": ["jest", "mocha", "cypress", "playwright"],
    "code_quality": ["black", "ruff", "flake8", "pylint", "pre-commit"],
    "security": ["owasp", "snyk", "sonarqube"],

    # PM / design / collaboration
    "ui_ux_design": ["figma", "sketch", "adobe xd", "invision", "balsamiq", "axure"],
    "issue_tracking": ["jira", "trello", "asana", "monday.com", "clickup", "linear"]
}

requirement_map = {
    "Bachelor of Technology in Computer Science": ["Bachelor of Technology in Computer Science","B.Tech CSE", "B.Tech in CS", "B.Tech CS", "B.Tech. (Computer Science)"],

    "Bachelor of Science in Computer Science": ["Bachelor of Science in Computer Science","B.S. CS", "B.Sc. CS", "BSCS", "Bachelor of Computer Science"],

    "Bachelor of Engineering in Computer Science": ["Bachelor of Engineering in Computer Science","B.E. CSE", "B.E. CS", "B.E. in Computer Science"],

    "Bachelor of Computer Applications": ["Bachelor of Computer Applications","BCA", "B.C.A.", "Bachelor in Computer Applications"],

    "Master of Technology in Computer Science": ["Master of Technology in Computer Science","M.Tech CSE", "M.Tech CS", "M.Tech in Computer Science"],

    "Master of Science in Computer Science": ["Master of Science in Computer Science","M.S. CS", "M.Sc. CS", "MSCS", "Master of Computer Science"],

    "Master of Computer Applications": ["Master of Computer Applications","MCA", "M.C.A.", "Master in Computer Applications"],

    "Doctor of Philosophy in Computer Science": ["Doctor of Philosophy in Computer Science","Ph.D. CS", "PhD in Computer Science", "Ph.D. in CSE"],

    "Bachelor's or Master's degree in Computer Science":[
    "Bachelor’s Master’s degree in Computer Science","Bachelor's Master's degree in Computer Science","Bachelor's Master's in computer science",
    "Bachelor’s Master’s in computer science"
    ]

    }