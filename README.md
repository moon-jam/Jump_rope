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

## Setup

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

## Configuration

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

## License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for more details.
