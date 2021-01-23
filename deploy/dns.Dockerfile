# builder
FROM golang:1.15-alpine as builder

WORKDIR /app

COPY ./go.mod .
COPY ./go.sum .

RUN go mod download

COPY . .

RUN go build -o /app/bin/dns cmd/main.go

# result container
FROM alpine

COPY --from=builder /app/bin/dns /app/dns

ENTRYPOINT ["/app/dns"]