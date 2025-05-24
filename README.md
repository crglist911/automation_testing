# automation_testing

## Running the Interactive Periodic Table

To view and interact with the periodic table, you need to serve the files using a local HTTP server. This is because modern web browsers have security restrictions that prevent fetching local JSON files (`elements.json`) when `index.html` is opened directly from the file system (via the `file:///` protocol).

### Using Python

If you have Python installed, you can use its built-in HTTP server.

1.  Open your terminal or command prompt.
2.  Navigate to the root directory of this project (where `index.html` is located).
3.  Run one of the following commands:
    *   For Python 3: `python3 -m http.server 8000` (or `python -m http.server 8000`)
    *   For Python 2: `python -m SimpleHTTPServer 8000`
4.  Open your web browser and go to: `http://localhost:8000`

The port number `8000` is an example; if it's in use, you can choose another one (e.g., 8080).

### Using Node.js

If you have Node.js and npm installed, you can use a simple command-line HTTP server like `http-server`.

1.  Install `http-server` globally (if you haven't already):
    ```bash
    npm install -g http-server
    ```
2.  Open your terminal or command prompt.
3.  Navigate to the root directory of this project.
4.  Run the command:
    ```bash
    http-server -p 8000
    ```
5.  Open your web browser and go to: `http://localhost:8000`

This will allow the `script.js` to correctly fetch and display the element data from `elements.json`.