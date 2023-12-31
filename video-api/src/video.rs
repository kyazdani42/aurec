use std::{fs, io::Error};

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct Video {
    name: String,
}

const MP4_END_BYTES: [u8; 92] = [
    0x74, 0x61, 0x00, 0x00, 0x00, 0x5a, 0x6d, 0x65, 0x74, 0x61, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x21, 0x68, 0x64, 0x6c, 0x72, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x6d, 0x64,
    0x69, 0x72, 0x61, 0x70, 0x70, 0x6c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x2d, 0x69, 0x6c, 0x73, 0x74, 0x00, 0x00, 0x00, 0x25, 0xa9, 0x74, 0x6f, 0x6f, 0x00,
    0x00, 0x00, 0x1d, 0x64, 0x61, 0x74, 0x61, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x4c,
    0x61, 0x76, 0x66, 0x35, 0x39, 0x2e, 0x32, 0x37, 0x2e, 0x31, 0x30, 0x30,
];

impl Video {
    pub fn from_readdir(p: Result<fs::DirEntry, Error>) -> Option<Self> {
        let p = p.ok()?;
        let fname = p.file_name().into_string().ok()?;
        let fbody = fs::read(p.path().to_str()?).ok()?;
        if fname.ends_with(".mp4") && fbody.ends_with(&MP4_END_BYTES) {
            Some(Video { name: fname })
        } else {
            None
        }
    }
}
