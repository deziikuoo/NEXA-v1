# Railway Deployment Checklist

## Pre-Deployment Checklist

### ✅ Environment Variables
Make sure these are set in Railway dashboard:
- `OPENAI_API_KEY` - Your OpenAI API key for GPT-4o
- `RAWG_API_KEY` - Your RAWG API key for game data
- `TWITCH_CLIENT_ID` - Your Twitch application client ID
- `TWITCH_CLIENT_SECRET` - Your Twitch application client secret
- `IGDB_CLIENT_ID` - (Optional) IGDB client ID (defaults to Twitch)
- `IGDB_CLIENT_SECRET` - (Optional) IGDB client secret (defaults to Twitch)

### ✅ Configuration Files
- `railway.json` - Railway deployment configuration
- `Procfile` - Process file for Railway
- `start.py` - Startup script
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification

## Deployment Steps

1. **Connect Repository**: Link your GitHub repository to Railway
2. **Set Environment Variables**: Add all required API keys in Railway dashboard
3. **Deploy**: Railway will automatically build and deploy
4. **Monitor Logs**: Check Railway logs for any startup issues

## Troubleshooting

### Health Check Fails
If the health check fails:

1. **Check Logs**: Look at Railway logs for error messages
2. **Verify Environment Variables**: Ensure all required API keys are set
3. **Test Locally**: Run `python start.py` locally to test startup
4. **Check Port**: Ensure the app listens on `$PORT` environment variable

### Common Issues

#### Issue: "Service unavailable" in health check
**Solution**: 
- Check if all environment variables are set
- Verify the startup script works locally
- Check Railway logs for Python import errors

#### Issue: Build fails
**Solution**:
- Ensure `requirements.txt` is up to date
- Check Python version compatibility
- Verify all dependencies are available

#### Issue: App starts but API calls fail
**Solution**:
- Verify API keys are correct
- Check API rate limits
- Test individual API endpoints

## Testing Deployment

1. **Health Check**: Visit `https://your-app.railway.app/`
2. **API Test**: Visit `https://your-app.railway.app/health`
3. **GPT-4o Test**: Visit `https://your-app.railway.app/api/test-gpt4o`

## Monitoring

- **Railway Dashboard**: Monitor resource usage and logs
- **Health Endpoint**: Check `/health` for service status
- **API Usage**: Monitor RAWG API usage in logs

## Rollback

If deployment fails:
1. Check Railway logs for specific errors
2. Fix issues in code
3. Push changes to trigger new deployment
4. Railway will automatically rollback if health checks fail 