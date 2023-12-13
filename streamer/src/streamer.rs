use actix_web::{web::Bytes, Error};
use futures::Stream;

use std::{
    env::var,
    fs::read,
    pin::Pin,
    task::{Context, Poll},
};

fn get_socket_location() -> Result<String, String> {
    var("AUREC_STREAM_SOCKET").map_err(|_| "AUREC_STREAM_SOCKET is required".to_owned())
}

pub struct Streamer {
    socket: String,
}

impl Streamer {
    pub fn new() -> Result<Self, String> {
        Ok(Streamer {
            socket: get_socket_location()?,
        })
    }
}

impl Stream for Streamer {
    type Item = Result<Bytes, Error>;

    fn poll_next(self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        if let Ok(f) = read(&self.socket) {
            Poll::Ready(Some(Ok(Bytes::from_iter(f))))
        } else {
            Poll::Ready(None)
        }
    }
}
