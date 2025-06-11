# Deployment Guide

This project can be deployed with minimal configuration using AWS for the Django backend and Vercel for the Vite/React frontend.

## Backend on AWS

1. Ensure `gunicorn`, `whitenoise`, and `django-cors-headers` are installed (already listed in `requirements.txt`).
2. Add environment variables defined in `.env.example` to your AWS deployment.
3. Deploy the app and run migrations. For Elastic Beanstalk:
   ```bash
   eb init -p python-3.11 your-app
   eb deploy
   eb ssh --command "python manage.py migrate"
   ```
4. Static files are served via WhiteNoise.

## Frontend on Vercel

1. From the `frontend/` directory run `npm run build` locally or let Vercel build it.
2. Configure the build output directory to `frontend/dist`.
3. Set the environment variable `VITE_API_BASE_URL` to the URL of the AWS deployment.

Once both services are deployed, the frontend will communicate with the backend via the configured API base URL.
