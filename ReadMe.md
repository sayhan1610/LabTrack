# LabTrack Equipment Management System

LabTrack is a comprehensive equipment management system designed for laboratory equipment tracking. It features functionalities for managing equipment, including adding, editing, searching, and bulk operations, as well as expiration alerts.

## Overview

- **Backend**: Powered by FastAPI and MongoDB.
- **Frontend**: A standalone application that manages interaction with the backend.

## Getting Started

### Backend Setup

1. **Prerequisites**

   - **Python 3.6.11 or later**: Ensure Python is installed on your system.
   - **MongoDB**: Setup Account and Clusters on [MongoDB's official website](https://www.mongodb.com/).
   - **FastAPI**: The backend is built using FastAPI. Make sure you have it installed.

2. **Clone the Repository**

   ```bash
   git clone https://github.com/sayhan1610/LabTrack.git
   cd LabTrack
   ```

3. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**

   Adjust the `MONGO_DETAILS` in `main.py`

   ```plaintext
   `MONGO_DETAILS = "mongo_db_url"`
   ```

6. **Run the Backend Server**

   ```bash
   python3 main.py
   ```

   or

   ```bash
   python main.py
   ```

### Frontend Setup

The frontend is provided as a standalone executable file. Follow these steps to use it:

1. **Go to /web**

   Simply navigate to the directory named `web`.

2. **Run the Application**

   - **Windows**: Double-click and run `start_labtrack_webui.exe` file.
   - **macOS/Linux**: Open a terminal **in the same directory** and use `python3 app.py` or `python app.py`.

3. **Configure API Base URL**

   Ensure the frontend is pointing to the correct backend URL. Open the frontend javascript and configure it to your own backend link. Setup `const apiBaseUrl = "url_here";`

## Features

- **View Equipment List**: Displays a table of all equipment with details.
- **Search Equipment**: Allows searching for equipment based on various parameters.
- **Add New Equipment**: Provides a form to add new equipment.
- **Bulk Add Equipment**: Facilitates adding multiple entries using JSON data.
- **Bulk Delete Equipment**: Allows deletion of multiple items based on IDs.
- **Edit Equipment**: Modify details of existing equipment.
- **Expiry Alert**: Alerts about items expiring within the next two weeks.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or support, please contact [sayhanrahman@gokkusagi.k12.tr](mailto:sayhanrahman@gokkusagi.k12.tr).

---

LabTrack © sayhan1610
