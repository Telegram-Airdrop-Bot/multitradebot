# 🚂 Railway.com Deployment Guide

## 📋 **Prerequisites**
- GitHub account with your repository
- Railway.com account
- API keys for Bybit and Pionex

## 🚀 **Step-by-Step Deployment**

### **1. Prepare Your Repository**
```bash
# Commit all changes
git add .
git commit -m "🚂 Add Railway deployment files"
git push origin main
```

### **2. Railway.com Setup**
1. **Go to:** [https://railway.app/](https://railway.app/)
2. **Sign up** with GitHub account
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository:** `Telegram-Airdrop-Bot/multitradebot`

### **3. Configure Environment Variables**
In Railway dashboard, go to **Variables** tab and add:

```bash
# Bybit API
BYBIT_API_KEY=your_actual_bybit_api_key
BYBIT_API_SECRET=your_actual_bybit_api_secret
BYBIT_TESTNET=false

# Pionex API
PIONEX_API_KEY=your_actual_pionex_api_key
PIONEX_SECRET_KEY=your_actual_pionex_secret_key

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_actual_bot_token
TELEGRAM_CHAT_ID=your_actual_chat_id

# App Settings
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=your_random_secret_key
```

### **4. Deploy Settings**
- **Build Command:** Leave empty (auto-detected)
- **Start Command:** `python gui_app.py`
- **Health Check Path:** `/health`

### **5. Deploy**
1. **Click "Deploy Now"**
2. **Wait for build** (usually 2-5 minutes)
3. **Check logs** for any errors
4. **Get your URL** from Railway dashboard

## 🔧 **Configuration Files Created**

### **Procfile**
```
web: python gui_app.py
```

### **railway.json**
```json
{
  "build": {"builder": "NIXPACKS"},
  "deploy": {
    "startCommand": "python gui_app.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300
  }
}
```

### **runtime.txt**
```
python-3.11.0
```

## 🌐 **Access Your Bot**

### **Railway URL Format:**
```
https://your-project-name.railway.app
```

### **Health Check:**
```
https://your-project-name.railway.app/health
```

## 📊 **Monitoring & Logs**

### **Railway Dashboard:**
- **Deployments** - View deployment history
- **Logs** - Real-time application logs
- **Metrics** - CPU, memory usage
- **Variables** - Environment variables

### **Health Check Endpoint:**
```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }
```

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **1. Build Failures**
- Check Python version compatibility
- Verify all dependencies in `requirements.txt`
- Check build logs for errors

#### **2. Runtime Errors**
- Verify environment variables are set
- Check application logs
- Ensure API keys are valid

#### **3. Port Issues**
- Railway automatically sets `PORT` environment variable
- Application uses `0.0.0.0` to accept external connections

### **Debug Commands:**
```bash
# Check Railway logs
railway logs

# Check environment variables
railway variables

# Restart deployment
railway up
```

## 💰 **Pricing & Limits**

### **Free Tier:**
- **500 hours/month** - Sufficient for development
- **Auto-sleep** when not in use
- **Custom domains** supported

### **Paid Plans:**
- **$5/month** - Always on, no sleep
- **$20/month** - Higher resource limits
- **Custom plans** for enterprise

## 🔒 **Security Best Practices**

### **Environment Variables:**
- **Never commit** API keys to repository
- **Use Railway variables** for sensitive data
- **Rotate keys** regularly

### **Production Settings:**
- **Debug mode disabled**
- **HTTPS enforced**
- **Health checks enabled**

## 📱 **Post-Deployment**

### **1. Test Your Bot:**
- Visit your Railway URL
- Test all features
- Check Telegram notifications

### **2. Set Custom Domain (Optional):**
- Go to **Settings** → **Domains**
- Add your custom domain
- Configure DNS records

### **3. Monitor Performance:**
- Check Railway metrics
- Monitor application logs
- Set up alerts if needed

## 🎯 **Success Checklist**

- [ ] Repository pushed to GitHub
- [ ] Railway project created
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] Health check passes
- [ ] Bot accessible via Railway URL
- [ ] All features working
- [ ] Telegram notifications working

## 🆘 **Support**

### **Railway Support:**
- **Documentation:** [docs.railway.app](https://docs.railway.app)
- **Discord:** [discord.gg/railway](https://discord.gg/railway)
- **Email:** support@railway.app

### **Your Bot Support:**
- **GitHub Issues:** Report bugs
- **Email:** moonbd01717@gmail.com
- **WhatsApp:** +8801701259687

---

**🚂 Happy Deploying on Railway!** 🎉 