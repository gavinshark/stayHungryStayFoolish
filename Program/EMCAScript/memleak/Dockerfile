FROM node:14.11

WORKDIR /app
ARG WKD="/app"
WORKDIR ${WKD}
COPY . ./

ENV PATH="${WKD}:${PATH}"

CMD ["node","memleak.js"]