# Selenium Pytest tests execution on Docker
Testing with **Selenium** can be tricky some times. Interacting with the DOM might be hard and it's full of undesired
behaviours.

One big problem when it comes to testing with **Selenium** is versioning and environment. Running tests with a specific
version of **Firefox** could work but it won't for another. These tests work on my **Mac** but they don't on this other **Debian**. The Python version I'm using on this host is different to yours.

**Docker** is the king of fixing this kind of problems. I though it could be a good idea to create a scenario where
tests were running faithfully and reliably.

Everything here has be only tested on **Elementary OS 5.1.5 Hera** (based on _Ubuntu 18.04_). I've used
**Docker 19.03.12**, **Docker Compose 1.26.1** and **Python 3.8.3**.

#### Tests
I've developed a small testing application under `selenium_tests/`. It uses **Pytest** as testing framework.
The tests are developed implementing a page object pattern.
They are run against the web _http://automationpractice.com_, which seems to be a webpage to use in cases like this.

## Running the tests locally (not recommended)
We are using Docker, so there's no need of running the tests locally. But if you really want it, here it is a how to:

1) Make sure you are on the `selenium_tests/` root.
2) Set a Python virtual environment. Activate it.
3) Install all the dependencies defined on `selenium_tests/requirements.txt` (`pip install -r requirements.txt`).
4) Download the last version of the Geckodriver (we will use Firefox as browser, so we assume you got it install on your system).
Running the following command will work:
`
wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz" -O /tmp/geckodriver.tgz && tar zxf /tmp/geckodriver.tgz -C ./selenium_tests/ && rm /tmp/geckodriver.tgz
`
5) Finally, simply run: `pytest`

## Running the tests using containers
### The images
#### selenium/hub and selenium/node-firefox
They complement each other. While the _selenium/hub_ deploys a container enabling a **Selenium Grid**, the
_selenium/node-firefox_ uses that grid and deploys a node with **Firefox** so tests can work using that browser.
A VNC server is also installed. To sum up, they will create the infrastructure where the tests will be run against.
You can read all the documentation about these images [here](https://github.com/SeleniumHQ/docker-selenium).

#### pytest-host
This image is defined on this repo `Dockerfile`. It consists on a _Ppython:3.8.3-alpine_ **Docker** image meaning that
the deployed container will be a very lightweight system (barely 100mB) with that Python version installed.

The image copies the contents of the `selenium_tests/` directory and install the Python packages defined on
`selenium_tests/requirements.txt`, so we set a perfect environment where to run the tests. It also downloads a script
named `wait-for-it.sh` and save it on the working directory. We'll talk about this on the following section.

Although as we'll see later there's no need, you could manually build an image by running the following on the repo root.
```
docker build -t "pytest-host:latest" .
```

### The orchestration
A `docker-compose.yml` is been also developed for making all the deployment process much easier. The three images
discussed above are defined as services here.

First of all the _pytest-host_ image is built. The _selenium/hub_ and _selenium/node-firefox_ containers are deployed
together. The first one exposes the port TCP/4444, where the grid is running. The _pytest-host_ container is waiting for the 
_selenium/node-firefox_ port 5555 to be ready to run the tests. This wait isn't natively implemented on **Docker Compose**.
That's why it's necessary to use third party scripts as the already mentioned
[wait-for-it.sh](https://github.com/vishnubob/wait-for-it).

A _bridge_ type network is also created and linked to all services so we make sure they all share the same network.
This is not strictly necessary since by default all services deployed using the same docker-compose project belongs to
[the same network](https://docs.docker.com/compose/networking/).

### The execution
There are several ways of running the tests using the developed **Docker** infrastructure.

#### Deploy the scenario and run all the tests
This is easily the simplest way of running your tests. Once your test files are up to date, you can run
```
docker-compose -p selenium_testing up --build --abort-on-container-exit --remove-orphans 
```
The _pytest-host_ image will always be built so new changes will be implemented. Then all the containers will be
deployed and the tests run.

Once you've finished working on this, run:
```
docker-compose down && docker system prune
```

Your system status will be the same as before starting the process.

#### Deploy the scenario and run only specific tests
Let's suppose you want to take advantage of this process but you don't need all the tests to be run.

Using our example, we will execute only the tests contained under the module `selenium_tests/tests/tests_searches.py`.
Run the following:
```
docker-compose build && docker-compose run --rm pytest-host pytest tests/test_searches.py -v --remote --rmt-host=selenium-hub --rmt-port=4444
```

If you ran the `docker-compose up` command before and receive an error message similar to
`ERROR: for selenium-hub  Cannot create container for service selenium-hub: Conflict`, stop and remove all the
containers involved. If you rather want to remove all the active containers, run:
```
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
```
