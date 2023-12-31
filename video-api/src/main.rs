use actix_web::{get, web, App, HttpResponse, HttpServer};

mod logger;
mod storage;
mod video;

struct Ctx {
    storage: storage::Storage,
    logger: logger::Logger,
}

#[get("/videos")]
async fn list_videos(ctx: web::Data<Ctx>) -> HttpResponse {
    match ctx.storage.list_videos() {
        Ok(video_list) => HttpResponse::Ok()
            .content_type("application/json")
            .json(video_list),
        Err(e) => {
            ctx.logger.log_err(e);
            HttpResponse::InternalServerError().into()
        }
    }
}

#[get("/videos/{id}")]
async fn serve_video(path: web::Path<String>, ctx: web::Data<Ctx>) -> HttpResponse {
    let selected_video_name = path.into_inner();
    match ctx.storage.get_video(selected_video_name) {
        Ok(video_bytes) => HttpResponse::Ok()
            .content_type("video/mp4")
            .body(video_bytes),
        Err(e) => {
            ctx.logger.log_err(e);
            HttpResponse::InternalServerError().into()
        }
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .app_data(web::Data::new(Ctx {
                storage: storage::Storage::new(),
                logger: logger::Logger::new(),
            }))
            .service(list_videos)
            .service(serve_video)
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}
