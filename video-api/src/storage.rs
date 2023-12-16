use std::fs::{read, read_dir};

use crate::video::Video;

pub struct Storage {
    video_location: String,
}

fn get_video_location() -> String {
    std::env::var("AUREC_VIDEO_LOCATION").unwrap_or("/tmp".into())
}

impl Storage {
    pub fn new() -> Self {
        Storage {
            video_location: get_video_location(),
        }
    }

    pub fn list_videos(&self) -> Result<Vec<Video>, String> {
        Ok(read_dir(&self.video_location)
            .map_err(|e| format!("Opening folder at location {}: {}", self.video_location, e))?
            .map(Video::from_readdir)
            .flatten()
            .collect())
    }

    pub fn get_video(&self, video_name: String) -> Result<Vec<u8>, String> {
        read(format!("{}/{}", self.video_location, video_name))
            .map_err(|e| format!("Could not get the video: {}", e))
    }
}
