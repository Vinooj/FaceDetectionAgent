# Face Detection and Identification

This project is a web-based application that performs face detection and identification. Users can upload an image with faces and then use a webcam to capture a new image. The application will then identify if the faces from the first image are present in the second.

## Features

*   **Face Detection**: Detects faces in an uploaded image using the RetinaFace model.
*   **Webcam Capture**: Captures an image from the user's webcam.
*   **Face Identification**: Compares the detected faces with the webcam capture to find matches.
*   **Web Interface**: A user-friendly web interface built with Streamlit.

## How It Works

The application consists of two main components:

1.  **Backend Server (`mcp_server.py`)**: A server built with `fastmcp` that exposes the face detection and identification functionality as a set of tools. It uses the `face_recognition` library to perform the core computer vision tasks.

2.  **Frontend Web Application (`app.py`)**: A Streamlit application that provides the user interface. It communicates with the backend server to perform the face detection and identification tasks.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    This project uses `uv` to manage dependencies. Make sure you have `uv` installed.
    ```bash
    uv venv
    source .venv/bin/activate
    uv sync
    ```

## Running the Application

To run the application, you need to start both the backend server and the frontend web application.

1.  **Start the backend server:**
    Open a terminal and run the following command:
    ```bash
    uv run mcp_server.py
    ```
    The server will start on `http://localhost:8000`.

2.  **Streamlit frontend web application:**
    Open another terminal and run the following command:
    ```bash
    streamlit run app.py
    ```
    The web application will be available at `http://localhost:8501`.

3. **Google Adk web Application:**
    ```bash
    adk web --port 9000
    ```
    open the ADK web URL in the browser. Say "Hi", say an follow the prompts.  

## Testing the Application that uses MCP Servers

To test the application using the `adk` tool, you can use the following commands.

1.  **Start the backend server:**
    ```bash
    uv run mcp_server.py
    ```
    This will start the MCP server on port 8000ß

2.  **Start the frontend with `adk`:**
    ```bash
    adk web --port 9000
    ```
    This will launch the web application on port 9000.
