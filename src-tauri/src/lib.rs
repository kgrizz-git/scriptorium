//! Scriptorium Tauri library entry.
//!
//! Hosts the desktop app runtime and shared Rust modules (book format types).
//! Tauri commands for ingest/load land in later milestones; M0 ships types only.

pub mod book_format;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
