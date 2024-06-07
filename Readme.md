# API Testing Tool by Evil Bane

## Overview

The API Testing Tool is a GUI application designed to facilitate testing of APIs. It allows users to send HTTP requests with customizable parameters such as URL, HTTP method, headers, and request data. The tool displays the response status code, headers, and content, and provides functionality to save and load requests, view request history, generate Python code for requests, and customize the application's theme.

## Features

- **Send HTTP Requests:** Supports GET, POST, PUT, and DELETE methods.
- **Custom Headers and Data:** Input custom request headers and data.
- **Response Display:** Shows status code, headers, and content of the response.
- **Request History:** Keeps a log of past requests.
- **Code Generation:** Generates Python code for the current request.
- **Save and Load Requests:** Save requests to a file and load them back.
- **Theme Customization:** Change the application's theme color.
- **Opening Animation:** Animated window opening.

## Installation

To run the API Testing Tool, you need Python installed on your machine. Follow the steps below to set up the application:

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/api-testing-tool.git
    cd api-testing-tool
    ```

2. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Run the application:**

    ```sh
    python api_testing_tool.py
    ```

## Usage

### Sending Requests

1. **URL:** Enter the API URL.
2. **HTTP Method:** Select the HTTP method (GET, POST, PUT, DELETE).
3. **Headers:** Enter request headers in `key:value` format, one per line.
4. **Data:** Enter request data for POST and PUT requests.
5. **Make Request:** Click the "Make Request" button to send the request and view the response.

### Response Display

- **Status Code:** Shows the HTTP status code of the response.
- **Response Headers:** Displays the headers of the response.
- **Response Content:** Shows the body of the response.

### Request History

- Logs all requests made during the session.
- Shows request method, URL, headers, and data.

### Code Generation

- Generates Python code for the current request.
- Copy the generated code for use in scripts.

### Save and Load Requests

- **Save Request:** Click "Save Request" to save the current request to a file.
- **Load Request:** Click "Load Request" to load a request from a file.

### Theme Customization

- **Change Theme:** Click the "Change Theme" button to select a new theme color.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.

## Author

Evil Bane

## Acknowledgements

Thanks to the developers of the `requests` library and the Tkinter team for their awesome work!

