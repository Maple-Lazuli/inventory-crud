# inventory-crud

## Getting Started

### DB and Backend

To start the database and backend, use the following command front the __root__ directory of the project

```
docker-compose -f docker-compose.yml up --build
```

This will start postgres in a docker container and the backend api in a second container.

### FrontEnd

To start the frontend, navigate to `inventory-crud/frontend/Inventory/` then run `npm install` from that directory.

After installation, run `npm run dev` to start the app. 

__note__: the frontend was created using react _vite_, which as a known issue of not being compatible with old versions of nodeJS.

## Details

The database used is POSGRES, with the following image being an entity relation diagram of the entities used.

![ERD](/assets/erd/erd.png)

The backend was created in Python using the flask module. 

The frontend was created in react Vite, with the start page captured below:

![ERD](/assets/erd/frontend.png)

The frontend could not be added to the docker compose due to an issue with vite confusing the host address with the docker container address. Attempts at using `--host`, explicitly exposing ports, and explicitly setting the IP address failed to correct this issue with vite.
