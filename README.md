# MGL869-IA-project

# The NodeJS MVC application

## How to run the backend

1. Run `npm install` in the root folder.
2. Run the server `node server`. Server is listening on 8080.
3. Open `http://localhost:8080/`

## How to run the frontend

1. Run `npm install` in the `frontend` folder.
2. Run the frontend `npm run dev`. Frontend is listening on port 5173.

# The observability stack

- Prometheus: `http://localhost:9090/`
- Grafana:  `http://localhost:3010/`
- Kibana: `https://localhost:5601/`
  Username=elastic / Password=changeme

# The fastAPIs

To build the fastAPIs docker images, you should first build the base image with the [fastAPI.base-image/Dockerfile]()
file.
You can use the following command from the folder `fastAPI.base-image`:

```bash
docker build -t fastapi-base-image .
```

Then, you can build the fastAPIs using the [docker-compose.yml]() file.

## Data processing

In order to work with the data processing fastAPI, you should first create two buckets in your MinIO instance `http://127.0.0.1:9001/browser`, by
default, the buckets are `images` and `training-data`. User is `minioadmin/minioadmin`.

Then start the api. If everything is ok, you should be able to access the api at `http://localhost:5010/docs` and a table
name images should have been created in the postgres database.

After that, you will need to fullfill the buckets with sample images to be able to test the pipeline. To do that, just
use the image of the dataset contains in `seg_pred` and add them to a folder named `images` in `setup_image`.
Then you can run `init-db-minio` which is in the same folder.

After that, wait for a while that all the images are loaded in the bucket. You can check the images by going to
`http://localhost:9001/` and logging in with the credentials `minioadmin:minioadmin` (defaults).

After doing so, you can run the pipeline directly from the data processing fastAPI.
The output images will appear in the other bucket named `training-data` (default).
