# Use Alpine-based Python image
FROM public.ecr.aws/lambda/python:3.10 AS base


COPY . ${LAMBDA_TASK_ROOT}

RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir
# Copy the source code into the container.

CMD ["main.lambda_handler"]