# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o server ./cmd/server

FROM gcr.io/distroless/base-debian12
COPY --from=build /app/server /server
ENTRYPOINT ["/server"]
