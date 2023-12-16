use std::{fs::DirEntry, io::Error};

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct Video {
    name: String,
}

impl Video {
    pub fn from_readdir(p: Result<DirEntry, Error>) -> Option<Self> {
        let fname = p.ok()?.file_name().into_string().ok()?;
        if fname.ends_with(".mp4") {
            Some(Video { name: fname })
        } else {
            None
        }
    }
}
