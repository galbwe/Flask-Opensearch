An example flask app to demonstrate building and querying an index.

## Setup

### Unix
- Install Docker
- In a terminal, change directories to `examples/simple_app` (the directory containing this README)
- Make sure you can execute all files in `examples/simple_app/scripts`
    ```
    chmod +x ./scripts/run.sh
    chmod +x ./scripts/load.sh
    chmod +x ./scripts/stop.sh
    ```
- Start the app with `./scripts/run.sh`
- Wait until you can see log output for the opensearch instance.
- In another terminal, cd to `examples/simple_app`, then run `./scripts/load.sh`. You should see a progress bar indicating how much movie data has been written to opensearch.
- Check that the REST endpoint for searching works with `curl "http://localhost:5000/movies?search=alien&count=3"`
- When you are done, run `./scripts/stop.sh`, or change to the terminal that is running the docker compose services and press `CTRL+C`

### Windows
- TODO