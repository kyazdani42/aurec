pub struct Logger {}

impl Logger {
    pub fn new() -> Self {
        Logger {}
    }

    pub fn log_err(&self, s: String) {
        eprintln!("{}", s);
    }
}
