use actix_web::{get, App, HttpResponse, HttpServer};

mod streamer;

#[get("/stream")]
async fn stream() -> HttpResponse {
    match streamer::Streamer::new() {
        Ok(streamer) => HttpResponse::Ok()
            .content_type("application/octet-stream")
            .streaming(streamer),
        Err(reason) => {
            println!("[AUREC] {}", reason);
            HttpResponse::InternalServerError().into()
        }
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().service(stream))
        .bind(("0.0.0.0", 8080))?
        .run()
        .await
}
