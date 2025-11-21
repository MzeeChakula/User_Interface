# Deploying MzeeChakula Backend to Render

## Quick Deploy

### Option 1: Deploy via Render Dashboard (Recommended)

1. **Push your code to GitHub** (if not already done)
   ```bash
   cd /home/dev-kiran/Projects/MzeeChakula/User_Interface/backend
   git add .
   git commit -m "Add Render deployment config"
   git push origin main
   ```

2. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Click "New +" → "Web Service"

3. **Connect Repository**
   - Connect your GitHub account
   - Select the `MzeeChakula` repository
   - Select the `User_Interface/backend` directory

4. **Configure Service**
   - **Name**: `mzeechakula-backend`
   - **Region**: Oregon (Free tier)
   - **Branch**: `main`
   - **Root Directory**: `User_Interface/backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables**
   Click "Advanced" → "Add Environment Variable" and add:
   
   ```
   DATABASE_URL=postgresql://postgres.viiuyzijqvigayaxghtd:[YOUR-PASSWORD]@...
   SECRET_KEY=xJJvoLEdbhaaBFX4gX9o3YeF6rEd_ad7bZlMFdlReDA
   GROQ_API_KEY=your-groq-api-key
   SUNBIRD_API_KEY=your-sunbird-api-key
   HUGGINGFACE_TOKEN=your-huggingface-token
   TAVILY_API_KEY=your-tavily-api-key
   SUPABASE_URL=https://viiuyzijqvigayaxghtd.supabase.co
   SUPABASE_KEY=your-supabase-anon-key
   CHROMA_PERSIST_DIR=./chroma_db
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   PYTHON_VERSION=3.12.0
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your API will be live at: `https://mzeechakula-backend.onrender.com`

### Option 2: Deploy via render.yaml (Infrastructure as Code)

1. **Push code with render.yaml**
   ```bash
   git add render.yaml
   git commit -m "Add render.yaml for deployment"
   git push origin main
   ```

2. **Create Blueprint**
   - Go to: https://dashboard.render.com/blueprints
   - Click "New Blueprint Instance"
   - Connect repository
   - Render will auto-detect `render.yaml`
   - Add your environment variables
   - Click "Apply"

## Post-Deployment

### 1. Verify Deployment

Visit your API documentation:
```
https://mzeechakula-backend.onrender.com/docs
```

### 2. Test Health Endpoint

```bash
curl https://mzeechakula-backend.onrender.com/health
```

### 3. Update Frontend

Update your frontend to use the Render URL:
```javascript
const API_URL = 'https://mzeechakula-backend.onrender.com'
```

## Important Notes

### Free Tier Limitations

- ⚠️ **Spins down after 15 minutes of inactivity**
- ⚠️ **First request after spin-down takes 30-60 seconds**
- ⚠️ **750 hours/month free** (enough for one service)

### Persistent Storage

- ⚠️ **ChromaDB data is ephemeral** on free tier
- Consider upgrading to paid plan for persistent disk
- Or use external vector DB (Pinecone, Weaviate)

### Database Connection

- ✅ Supabase works perfectly with Render
- ✅ Connection pooling is handled by Supabase
- ✅ No additional configuration needed

## Troubleshooting

### Build Fails

If build fails, check:
1. `requirements.txt` is in the root directory
2. Python version matches `runtime.txt`
3. All dependencies are listed

### Service Won't Start

Check logs in Render dashboard:
- Look for missing environment variables
- Check for import errors
- Verify database connection

### Slow First Request

This is normal on free tier. Solutions:
1. Use a paid plan ($7/month)
2. Use a cron job to ping every 14 minutes
3. Accept the cold start delay

## Monitoring

### View Logs

```bash
# In Render Dashboard
Services → mzeechakula-backend → Logs
```

### Set Up Alerts

- Go to Settings → Notifications
- Add email for deployment failures
- Add Slack webhook (optional)

## Scaling

### Upgrade to Paid Plan

For production, consider:
- **Starter Plan**: $7/month
  - No spin-down
  - Faster deployment
  - Better performance

- **Standard Plan**: $25/month
  - Horizontal scaling
  - More memory/CPU
  - Persistent disk

## Custom Domain

1. Go to Settings → Custom Domain
2. Add your domain: `api.mzeechakula.com`
3. Update DNS records as shown
4. SSL certificate auto-provisioned

## CI/CD

Render automatically deploys when you push to `main`:
```bash
git push origin main
# Render detects push and deploys automatically
```

## Environment Variables Management

### Update Variables

1. Go to Environment tab
2. Edit variables
3. Click "Save Changes"
4. Service auto-restarts

### Secret Management

For sensitive data:
- Use Render's built-in secret storage
- Never commit secrets to Git
- Use `.env.example` for documentation

## Your Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Connect GitHub repository
- [ ] Configure web service
- [ ] Add all environment variables
- [ ] Deploy service
- [ ] Test `/health` endpoint
- [ ] Test `/docs` endpoint
- [ ] Update frontend API URL
- [ ] Test full integration
- [ ] Set up monitoring/alerts

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Status Page: https://status.render.com
