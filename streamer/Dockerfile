FROM rust:1.74.0 AS build

COPY Cargo.toml Cargo.lock /app/

WORKDIR /app
RUN mkdir -p src && echo "fn main() {}" > src/lib.rs
RUN cargo build --release

COPY ./src /app/src
RUN touch src/main.rs
RUN cargo install --path .

FROM debian:latest AS run

COPY --from=build /usr/local/cargo/bin/streamer /usr/bin/streamer

EXPOSE 8080

CMD streamer
