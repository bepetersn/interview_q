# Deployment Guide

This project can be deployed with minimal configuration using Heroku for the Django backend and Vercel for the Vite/React frontend.

## Backend on Heroku

1. Ensure `gunicorn`, `whitenoise`, and `django-cors-headers` are installed (already listed in `requirements.txt`).
2. Add environment variables defined in `.env.example` to your Heroku app.
3. Deploy the app and run migrations:
   ```bash
   heroku create
   git push heroku main
   heroku run python manage.py migrate
   ```
4. Collect static files automatically via WhiteNoise.

## Frontend on Vercel

1. From the `frontend/` directory run `npm run build` locally or let Vercel build it.
2. Configure the build output directory to `frontend/dist`.
3. Set the environment variable `VITE_API_BASE_URL` to the URL of the Heroku deployment.

Once both services are deployed, the frontend will communicate with the backend via the configured API base URL.
