# Jump Rope League

## Overview

Jump Rope League is an innovative web application designed to enhance the experience of jump rope enthusiasts. It allows users to upload videos of their jump rope routines, get them analyzed for performance, and receive scores based on their skills. The platform encourages users to compete and improve by providing a ranking system and various interactive features.

## Features

- **Video Upload**: Users can upload their jump rope videos to participate in the league.
- **Performance Analysis with Machine Learning**: This app uses machine learning to analyze videos. It uses a YOLOv8-trained model to see what the jumper is doing. It also uses segmentation to find where the rope is. Although the rope's position currently isn't used for counting jumps, it would enhance the app in the future.
- **Ranking System**: Users can see their rankings based on the scores from their videos.
- **User Authentication**: Secure sign-in functionality with Google OAuth.
- **Dark Mode**: A toggle switch for users to switch between light and dark modes for better usability.
- **Responsive Design**: Ensures a consistent experience across various devices and screen sizes.

## Configuration

Before running the application, you need to configure several files:

1. **config.py**: This file contains configuration for the Flask application. You can use [`config_template.py`](./config_template.py) as a starting point. You need to set `app_secret_key` which is used as the secret key in Flask. You also need to set `CLIENT_ID` and `CLIENT_SECRET` which are used for Google OAuth. Rename `config_template.py` to `config.py` after setting your information.

2. **server.csr and server.key**: These files are used for HTTPS SSL configuration. You can use [`server_template.csr`](./server_template.csr) and [`server_template.key`](./server_template.key) as starting points. You need to generate these files and place them in the appropriate location. Rename `server_template.csr` and `server_template.key` to `server.csr` and `server.key` respectively after setting your information.

Please make sure to update these files with your own information before running the application.

## Setup

Before setting up the environment and running the application, make sure you have completed the above configuration steps.

### Local Python/Virtual Environment

1. **Clone the Repository**:

   ```bash
   git clone https://your-repository-url
   cd Jump_rope
   ```

2. **Create and Activate Virtual Environment**:
   - For Linux/Mac:

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

   - For Windows:

     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:

   ```bash
   python app.py
   ```

### Docker

1. **Build the Docker Image**:

   ```bash
   docker build -t jump_rope .
   ```

2. **Run the Docker Container**:

   ```bash
   docker run -p 5000:5000 jump_rope
   ```

## Deployment

### Gunicorn (Linux/Mac)

- Run the app using Gunicorn:

  ```bash
  gunicorn --config gunicorn.conf.py wsgi:app
  ```

### Waitress (Windows)

- Run the app using Waitress:

  ```bash
  waitress-serve --port=5000 wsgi:app
  ```

### Python Direct Execution (Less Stable)

- Run the app directly using Python (not recommended for production):

  ```bash
  python app.py
  ```

### Using Docker

- Ensure Docker daemon is running and use the Docker commands listed in the Setup section.

## FAQ

### How do I apply for Google OAuth?

To apply for Google OAuth, follow these steps:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).

2. Create a new project or select an existing one.

3. In the sidebar, click on "APIs & Services" and then "Credentials".

4. Click on "Create Credentials" and select "OAuth client ID".

5. If you haven't configured the consent screen yet, you'll be prompted to do so. Fill in the necessary information.

6. After configuring the consent screen, select "Web application" as the application type. Enter the name for your OAuth client ID.

7. Under "Authorized redirect URIs", enter the URI where you'll be redirected after the authentication process. For local development, this is usually `http://localhost:5000/`.

8. Click "Create". You'll be given a client ID and a client secret. Use these in your `config.py` file.

## License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for more details.
