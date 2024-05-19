// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

#[tauri::command]
fn write_to_file(path: &str, contents: &str) -> Result<(), String> {
    std::fs::write(path, contents).map_err(|e| e.to_string())
}

fn main() {
  tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![write_to_file])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
