# Authoring Tool

## Description
This tool enables the upload and annotation of 3D models, which can then be integrated into a Unity scene. Additionally, it supports adding PDFs to enhance the knowledge base for LLMs. It is built using SvelteKit and Tauri.


## Getting Started

### Prerequisites

To use this tool, you need to have the following installed on your system:

- [Node.js](https://nodejs.org/) for running the application.
- [Rust (optional)](https://www.rust-lang.org/tools/install) for building the standalone desktop application with Tauri.


### Running as a Web Application

To run the tool as a web application, use the following command:

```bash
npm run dev
```

### Running as a Standalone Desktop Application

To run the tool as a standalone desktop application using Tauri, use the following command:

```bash
npm run tauri dev
```

**Note**: To run the standalone application, you need to have [Rust](https://www.rust-lang.org/tools/install) installed on your system, as Tauri relies on Rust for its backend.

## Credits

- Skybox: [Autumn Field Puresky](https://polyhaven.com/a/autumn_field_puresky) provided by Poly Haven.
- Sample Model: [Cafeteria 3D Model](https://sketchfab.com/3d-models/cafeteria-36c07861716c428bba658b9845f14f03) available on Sketchfab.
