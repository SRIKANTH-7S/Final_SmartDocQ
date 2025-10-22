# SmartDocQ Deployment Guide

This guide will help you deploy your SmartDocQ application to Render.

## Prerequisites

- GitHub account
- Render account (free tier available)
- MongoDB Atlas account (for production database)

## Project Structure

```
smartdocq/
├── client/          # React frontend (Vite + TypeScript)
├── server/          # Node.js backend (Express + TypeScript)
├── package.json     # Root package.json for build management
├── build.js         # Build script
├── render.yaml      # Render configuration
└── DEPLOYMENT.md    # This file
```

## Step-by-Step Deployment

### 1. Prepare Your Code

1. **Commit all changes to Git:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Test the build locally:**
   ```bash
   npm run build
   ```

### 2. Set Up MongoDB Atlas (Database)

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free cluster
3. Create a database user
4. Whitelist all IP addresses (0.0.0.0/0) for Render
5. Get your connection string

### 3. Deploy to Render

#### Option A: Using Render Dashboard (Recommended)

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**
   - **Name:** `smartdocq` (or your preferred name)
   - **Environment:** `Node`
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Root Directory:** Leave empty (uses root)
   - **Build Command:** `npm run build`
   - **Start Command:** `npm start`

5. **Set Environment Variables:**
   ```
   NODE_ENV=production
   PORT=10000
   HOST=0.0.0.0
   MONGO_URI=your_mongodb_atlas_connection_string
   JWT_SECRET=your_super_secret_jwt_key_here
   JWT_EXPIRY_MINUTES=60
   ALLOWED_ORIGINS=https://your-app-name.onrender.com
   GOOGLE_AI_API_KEY=your_google_ai_api_key_here
   ```

6. **Click "Create Web Service"**

#### Option B: Using render.yaml (Advanced)

1. **Push your code with render.yaml to GitHub**
2. **In Render Dashboard, click "New +" → "Blueprint"**
3. **Connect your repository**
4. **Render will automatically detect render.yaml and configure everything**

### 4. Configure Database

1. **In Render Dashboard, go to your service**
2. **Click "Environment" tab**
3. **Add your MongoDB connection string:**
   ```
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/smartdocq?retryWrites=true&w=majority
   ```

### 5. Test Your Deployment

1. **Wait for deployment to complete (5-10 minutes)**
2. **Visit your app URL:** `https://your-app-name.onrender.com`
3. **Test the health endpoint:** `https://your-app-name.onrender.com/api/health`

## Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `NODE_ENV` | Environment mode | Yes | `production` |
| `PORT` | Server port | Yes | `10000` |
| `HOST` | Server host | Yes | `0.0.0.0` |
| `MONGO_URI` | MongoDB connection string | Yes | `mongodb+srv://...` |
| `JWT_SECRET` | JWT signing secret | Yes | `your-secret-key` |
| `JWT_EXPIRY_MINUTES` | JWT token expiry | No | `60` |
| `ALLOWED_ORIGINS` | CORS allowed origins | Yes | `https://your-app.onrender.com` |
| `GOOGLE_AI_API_KEY` | Google AI API key | No | `your-api-key` |

## Troubleshooting

### Common Issues

1. **Build Fails:**
   - Check Node.js version (requires 18+)
   - Ensure all dependencies are in package.json
   - Check build logs in Render dashboard

2. **App Won't Start:**
   - Verify environment variables are set
   - Check MongoDB connection string
   - Review server logs

3. **CORS Errors:**
   - Update `ALLOWED_ORIGINS` with your actual domain
   - Check if frontend is making requests to correct API endpoints

4. **Database Connection Issues:**
   - Verify MongoDB Atlas cluster is running
   - Check IP whitelist includes 0.0.0.0/0
   - Verify connection string format

### Checking Logs

1. **In Render Dashboard:**
   - Go to your service
   - Click "Logs" tab
   - Check for error messages

2. **Common Log Locations:**
   - Build logs: Shows during deployment
   - Runtime logs: Shows when app is running

## Performance Optimization

### For Production

1. **Enable Gzip compression** (already configured)
2. **Set up CDN** for static assets
3. **Configure caching headers**
4. **Monitor memory usage**

### Scaling

- **Free tier:** 750 hours/month, sleeps after 15 minutes of inactivity
- **Paid tiers:** Always-on, better performance, custom domains

## Security Considerations

1. **Never commit secrets to Git**
2. **Use strong JWT secrets**
3. **Configure CORS properly**
4. **Use HTTPS in production**
5. **Regularly update dependencies**

## Monitoring

1. **Render provides basic monitoring**
2. **Set up uptime monitoring** (UptimeRobot, Pingdom)
3. **Monitor database performance** in MongoDB Atlas
4. **Set up error tracking** (Sentry, LogRocket)

## Support

- **Render Documentation:** https://render.com/docs
- **MongoDB Atlas:** https://docs.atlas.mongodb.com
- **Project Issues:** Create GitHub issue

---

**Happy Deploying! 🚀**
