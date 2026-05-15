## CineMatch - Movie Recommendation System

### Overview

- A movie recommendation web application (used to be) built as part of [The Odin Project](https://www.theodinproject.com/lessons/node-path-react-new-shopping-cart)
  curriculum. Now it serves as the API for [CineMatch Client](https://github.com/zadnap/cinematch-client) and uses [CineMatch ML Service](https://github.com/zadnap/cinematch-ml-service) as its recommendation core.
- This project focuses on building a movie recommendation API by integrating MovieLens and TMDB data, implementing content-based and hybrid recommendation techniques, and designing a scalable backend service using Flask to deliver personalized movie suggestions.
- See the project in action: [CineMatch](https://cinematch-client.vercel.app).

### Installation & Usage

1. Clone repository

   ```bash
   git clone https://github.com/zadnap/cinematch-api.git
   ```

2. Create virtual environment

   ```bash
   python3.11 -m venv venv
   ```

3. Activate virtual environment

- macOS / Linux:

  ```bash
  source venv/bin/activate
  ```

- Windows:

  ```bash
  venv\Scripts\activate
  ```

4. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

5. Create an .env file with content

   ```bash
   JWT_SECRET_KEY=<your_jwt_secret_key>
   DATABASE_URI=<your_db_uri>
   TMDB_API_KEY=<your_tmdb_api_key>
   CORS_ORIGINS=<client_url>,<ml_service_url>
   ML_SERVICE_URL=<ml_service_url>
   ```

6. Run the server

   ```bash
   flask run
   ```
