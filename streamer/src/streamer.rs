use actix_web::{
    rt::{spawn, time},
    web::Bytes,
    Error,
};
use futures::task::Waker;
use futures::Stream;

use std::{
    env::var,
    fs::read,
    pin::Pin,
    task::{Context, Poll},
    time::Duration,
};

fn get_socket_location() -> Result<String, String> {
    var("AUREC_STREAM_SOCKET").map_err(|_| "AUREC_STREAM_SOCKET is required".to_owned())
}

pub struct Streamer {
    socket: String,
    bytes_read: usize,
    wait_next: bool,
}

impl Streamer {
    pub fn new() -> Result<Self, String> {
        Ok(Streamer {
            socket: get_socket_location()?,
            bytes_read: 0,
            wait_next: false,
        })
    }

    fn wake_later(&self, waker: &Waker) {
        let waker = waker.clone();
        spawn(async move {
            time::sleep(Duration::from_millis(20)).await;
            waker.wake_by_ref();
        });
    }
}

const MAX_BYTES_READ: usize = 10_000_000;

impl Stream for Streamer {
    type Item = Result<Bytes, Error>;

    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        if self.bytes_read > MAX_BYTES_READ {
            return Poll::Ready(None);
        }

        if self.wait_next {
            self.wake_later(cx.waker());
            self.get_mut().wait_next = false;
            return Poll::Pending;
        }

        if let Ok(f) = read(&self.socket) {
            if f.len() == 0 {
                self.wake_later(cx.waker());
                return Poll::Pending;
            }

            let this = self.get_mut();
            this.bytes_read = this.bytes_read + f.len();
            this.wait_next = true;

            Poll::Ready(Some(Ok(Bytes::from_iter(f))))
        } else {
            Poll::Ready(None)
        }
    }
}
