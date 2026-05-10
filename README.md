## CineMatch - Movie Recommendation System

### Overview

- A shopping cart web application (used to be) built as part of [The Odin Project](https://www.theodinproject.com/lessons/node-path-react-new-shopping-cart)
  curriculum. Now it serves as the API for [CineMatch Client](https://github.com/zadnap/cinematch-client).
- This project focuses on building a movie recommendation API by integrating MovieLens and TMDB data, implementing content-based and hybrid recommendation techniques, and designing a scalable backend service using Flask to deliver personalized movie suggestions.
- See the project in action: [CineMatch](https://cinematch-client-xi-liart.vercel.app/).

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

5. Run the server

   ```bash
   flask run
   ```
