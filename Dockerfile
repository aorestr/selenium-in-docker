FROM python:3.8.3-alpine

# Set the working directory
WORKDIR /selenium_tests/

# Copy the folder with the tests into the container
COPY selenium_tests/ /selenium_tests/

# Install all dependencies
RUN pip install -r requirements.txt

# Run the tests
CMD ["pytest", "--remote"]