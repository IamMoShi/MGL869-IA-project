# MGL869-IA-project

# The NodeJS MVC application

## How to run the web-server

1. Run `npm install` in the root folder.
2. Build the docker using the [docker-compose.yml]() file.
3. The frontend should be available at `http://localhost:3000/`.

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

Then, you have to put the `images` bucket in download status (read access for all users)

```bash
mc alias set local http://localhost:9000 minioadmin minioadmin
mc admin policy create local readonly-policy minio-policy.json 
mc anonymous set download local/images 
```

Then start the api. If everything is ok, you should be able to access the api at `http://localhost:5010/docs` and a table
name images should have been created in the postgres database.

After that, you will need to fullfill the buckets with sample images to be able to test the pipeline. To do that, just
use the image of the dataset contains in `seg_pred` and add them to a folder named `images` under folder `setup_image`.
Then you can run `init-db-minio` which is in the same folder. That will copy images in the minio bucket and create entries in the postgreSQL BD with their categories.

After that, wait for a while that all the images are loaded in the bucket. You can check the images by going to
`http://localhost:9001/` and logging in with the credentials `minioadmin:minioadmin` (defaults).

After doing so, you can run the pipeline directly from the data processing fastAPI.
The output images will appear in the other bucket named `training-data` (default).
