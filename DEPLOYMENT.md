# Deploying the QR Code Generator to Vercel

This guide explains how to deploy the QR Code Generator to Vercel as a serverless application without a database.

## Prerequisites

- A GitHub account
- A Vercel account (can sign up with GitHub)
- Your QR Code Generator project pushed to a GitHub repository

## Environment Setup

1. Copy the example environment file:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file to set your environment variables:
   ```
   # For development
   ENVIRONMENT=development
   ALLOWED_ORIGINS=*
   
   # For production deployment
   # ENVIRONMENT=production
   # ALLOWED_ORIGINS=https://your-production-url.com
   ```

## Deployment Steps

1. Push your code to a GitHub repository.

2. Connect the repository to Vercel:
   - Sign in to Vercel and click "New Project"
   - Import your GitHub repository
   - Configure the project:
     - Framework Preset: Other
     - Root Directory: ./
     - Build Command: None (leave empty)
     - Output Directory: src/frontend

3. Set environment variables in the Vercel dashboard:
   - `ENVIRONMENT`: Set to `production`
   - `ALLOWED_ORIGINS`: Set to your production domain

4. Deploy the project.

## Deployment Configuration

The project includes a `vercel.json` file that configures:
- Python backend as a serverless function
- Static frontend files
- API routing
- Environment variables

```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/backend/api.py",
      "use": "@vercel/python"
    },
    {
      "src": "src/frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "src/backend/api.py"
    },
    {
      "src": "/(.*)",
      "dest": "src/frontend/html/$1"
    }
  ],
  "env": {
    "ENVIRONMENT": "production",
    "ALLOWED_ORIGINS": "https://your-production-url.com"
  }
}
```

## Serverless Considerations

The application has been optimized for serverless deployment:

1. **In-memory Storage**: Instead of using the file system for storing QR codes, the application uses in-memory storage.

2. **Temporary Files**: For QR code generation, temporary files are used and then cleaned up.

3. **Environment Detection**: The frontend JavaScript detects whether it's running in production or development and uses the appropriate API endpoints.

4. **CORS Configuration**: The API is configured to accept requests from specified origins.

5. **Stateless Operation**: The application is designed to be stateless, which is ideal for serverless functions.

## Troubleshooting

If you encounter issues with your deployment:

1. **Check Logs**: Vercel provides logs for each deployment and function execution.

2. **Environment Variables**: Ensure all required environment variables are set correctly.

3. **CORS Issues**: If you're experiencing CORS errors, check that the `ALLOWED_ORIGINS` environment variable is set correctly.

4. **Function Timeouts**: Serverless functions have execution time limits. If your QR code generation is taking too long, consider optimizing the process.

5. **Memory Usage**: Serverless functions also have memory limits. Monitor your application's memory usage.

## Local Testing

Before deploying, you can test your application locally:

1. Set up the environment variables in your `.env` file.

2. Install the required packages:
   ```
   pip install -r src/backend/requirements.txt
   ```

3. Run the Flask API:
   ```
   cd src/backend
   python api.py
   ```

4. Access the application at http://localhost:5000
