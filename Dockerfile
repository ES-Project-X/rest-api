FROM python:3.11-alpine

WORKDIR /code

COPY . .

# Build arguments environment variables
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG BUCKET_NAME
ARG COGNITO_APP_CLIENT_ID
ARG COGNITO_USERPOLL_ID
ARG FRONTEND_URL
ARG POSTGRES_DB
ARG POSTGRES_HOST
ARG POSTGRES_PASSWORD
ARG POSTGRES_PORT
ARG POSTGRES_USER

RUN echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" > .env && \
    echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> .env && \
    echo "BUCKET_NAME=$BUCKET_NAME" >> .env && \
    echo "COGNITO_APP_CLIENT_ID=$COGNITO_APP_CLIENT_ID" >> .env && \
    echo "COGNITO_USERPOLL_ID=$COGNITO_USERPOLL_ID" >> .env && \
    echo "FRONTEND_URL=$FRONTEND_URL" >> .env && \
    echo "POSTGRES_DB=$POSTGRES_DB" >> .env && \
    echo "POSTGRES_HOST=$POSTGRES_HOST" >> .env && \
    echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> .env && \
    echo "POSTGRES_PORT=$POSTGRES_PORT" >> .env && \
    echo "POSTGRES_USER=$POSTGRES_USER" >> .env


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
