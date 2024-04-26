# Imagination API

Azure Function App that uses the [Imagination APP](https://github.com/diegohumpire/imagination-app) to generate images with GPT and Dall-E.

## Requirements

-   Python 3.11

## Environment Variables

Make a copy of the `local.settings.json.example` file and rename it to `local.settings.json`. Fill in the values for the environment variables.

```json
{
    "IsEncrypted": false,
    "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
        "REDIS_HOST": "",
        "REDIS_PASSWORD": "",
        "OPENAI_API_KEY": ""
    }
}
```

Fill in the values for the environment variables:

-   `REDIS_HOST`: The host of the Redis server.
-   `REDIS_PASSWORD`: The password of the Redis server.
-   `OPENAI_API_KEY`: The API key for the OpenAI API.

If you will deploy the function app to Azure, you can set the environment variables in the Azure portal.

## Dependencies

-   FastAPI
-   Azure Functions
-   Redis
-   OpenAI API

## How to run

1.  Setup virtual env and install the dependencies

Linux or MacOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2.  Run the Azure Function App

```bash
func host start
```

## Debugging

To debug the Azure Function App, you can use the `Python: Attach to Remote Container` configuration in VSCode. This will attach the debugger to the running container.

Press F5 to start debugging on VS code.
