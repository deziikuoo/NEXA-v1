# 🚀 Deployment Guide

This guide covers various deployment options for NEXA Game Recommender.

## 🌐 Live Demo

**🎮 Try the live application**: [https://nexa-pro.up.railway.app](https://nexa-pro.up.railway.app)

## 📋 Prerequisites

Before deploying, ensure you have:

- [ ] All required API keys configured
- [ ] Environment variables set up
- [ ] Domain name (optional but recommended)
- [ ] SSL certificate (for production)

## 🔧 Environment Variables

Set these environment variables in your deployment platform:

```env
# Required
OPENAI_API_KEY=your_openai_api_key
RAWG_API_KEY=your_rawg_api_key
TWITCH_CLIENT_ID=your_twitch_client_id
TWITCH_CLIENT_SECRET=your_twitch_client_secret

# Optional
IGDB_CLIENT_ID=your_igdb_client_id
IGDB_CLIENT_SECRET=your_igdb_client_secret
PORT=8000
NODE_ENV=production
```

## 🚂 Railway Deployment (Recommended)

### Automatic Deployment

1. **Fork the repository** to your GitHub account
2. **Connect to Railway**:
   - Visit [Railway](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your forked repository
3. **Set environment variables** in Railway dashboard
4. **Deploy!** Railway will automatically build and deploy

### Manual Deployment

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Set environment variables
railway variables set OPENAI_API_KEY=your_key
railway variables set RAWG_API_KEY=your_key
railway variables set TWITCH_CLIENT_ID=your_id
railway variables set TWITCH_CLIENT_SECRET=your_secret

# Deploy
railway up
```

## 🐳 Docker Deployment

### Local Docker

```bash
# Build the image
docker build -t nexa-game-recommender .

# Run the container
docker run -p 8000:8000 --env-file .env nexa-game-recommender
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  nexa:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - RAWG_API_KEY=${RAWG_API_KEY}
      - TWITCH_CLIENT_ID=${TWITCH_CLIENT_ID}
      - TWITCH_CLIENT_SECRET=${TWITCH_CLIENT_SECRET}
    env_file:
      - .env
```

Run with:
```bash
docker-compose up -d
```

### Docker Hub

```bash
# Build and tag
docker build -t yourusername/nexa-game-recommender:latest .

# Push to Docker Hub
docker push yourusername/nexa-game-recommender:latest

# Pull and run
docker pull yourusername/nexa-game-recommender:latest
docker run -p 8000:8000 --env-file .env yourusername/nexa-game-recommender:latest
```

## ☁️ Cloud Platform Deployment

### Heroku

1. **Install Heroku CLI**:
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy**:
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create your-nexa-app
   
   # Set environment variables
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set RAWG_API_KEY=your_key
   heroku config:set TWITCH_CLIENT_ID=your_id
   heroku config:set TWITCH_CLIENT_SECRET=your_secret
   
   # Deploy
   git push heroku main
   ```

### Google Cloud Platform (GCP)

1. **Install Google Cloud SDK**
2. **Create project and enable APIs**
3. **Deploy to Cloud Run**:

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/nexa-game-recommender

# Deploy to Cloud Run
gcloud run deploy nexa-game-recommender \
  --image gcr.io/PROJECT_ID/nexa-game-recommender \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key,RAWG_API_KEY=your_key
```

### AWS

#### AWS Elastic Beanstalk

1. **Install EB CLI**:
   ```bash
   pip install awsebcli
   ```

2. **Initialize and deploy**:
   ```bash
   eb init
   eb create nexa-production
   eb deploy
   ```

#### AWS ECS

1. **Create ECR repository**:
   ```bash
   aws ecr create-repository --repository-name nexa-game-recommender
   ```

2. **Build and push**:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
   docker build -t nexa-game-recommender .
   docker tag nexa-game-recommender:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/nexa-game-recommender:latest
   docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/nexa-game-recommender:latest
   ```

3. **Create ECS service** (via AWS Console or CLI)

### Azure

#### Azure Container Instances

```bash
# Build and push to Azure Container Registry
az acr build --registry yourregistry --image nexa-game-recommender .

# Deploy to Container Instances
az container create \
  --resource-group your-rg \
  --name nexa-game-recommender \
  --image yourregistry.azurecr.io/nexa-game-recommender:latest \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=your_key RAWG_API_KEY=your_key
```

## 🖥️ VPS Deployment

### Ubuntu/Debian

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone https://github.com/deziikuoo/NEXA-v1.git
cd NEXA-v1

# Set up environment variables
cp .env.example .env
nano .env  # Edit with your API keys

# Deploy with Docker Compose
docker-compose up -d
```

### Nginx Configuration

Create `/etc/nginx/sites-available/nexa`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/nexa /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 SSL/HTTPS Setup

### Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Cloudflare (Recommended)

1. **Add domain to Cloudflare**
2. **Update nameservers**
3. **Enable SSL/TLS encryption mode: Full**
4. **Set up page rules for caching**

## 📊 Monitoring and Logging

### Health Checks

The application includes health check endpoints:

- `GET /health` - Basic health check
- `GET /api/test-gpt4o` - Test GPT-4o integration

### Logging

Configure logging in your deployment:

```python
# In app_fastapi.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Monitoring Tools

- **Uptime Robot**: Free uptime monitoring
- **Sentry**: Error tracking and performance monitoring
- **New Relic**: Application performance monitoring
- **Datadog**: Infrastructure monitoring

## 🔄 CI/CD Pipeline

The repository includes GitHub Actions for automated deployment:

- **Push to main**: Deploy to production
- **Push to develop**: Deploy to staging
- **Pull requests**: Run tests and security scans

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   sudo lsof -i :8000
   sudo kill -9 <PID>
   ```

2. **Environment variables not set**:
   ```bash
   # Check environment variables
   printenv | grep -E "(OPENAI|RAWG|TWITCH)"
   ```

3. **Docker build fails**:
   ```bash
   # Clean Docker cache
   docker system prune -a
   ```

4. **API rate limits**:
   - Check API key limits
   - Implement proper rate limiting
   - Use caching where possible

### Performance Optimization

1. **Enable caching**:
   ```python
   from fastapi_cache import FastAPICache
   from fastapi_cache.backends.redis import RedisBackend
   ```

2. **Database optimization** (if using database):
   - Add indexes
   - Optimize queries
   - Use connection pooling

3. **CDN setup**:
   - Use Cloudflare or similar CDN
   - Cache static assets
   - Enable compression

## 📞 Support

For deployment issues:

- **GitHub Issues**: [Create an issue](https://github.com/deziikuoo/NEXA-v1/issues)
- **Documentation**: Check the main [README.md](../README.md)
- **Community**: Join our [Discussions](https://github.com/deziikuoo/NEXA-v1/discussions)

---

**Happy deploying! 🚀** 