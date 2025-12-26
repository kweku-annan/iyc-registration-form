# IYC Conference Registration Website

A modern, professional conference attendee registration website with Google Sheets integration and SMS confirmation. Built with a stunning gold, black, and white color scheme.

## 🌟 Features

- **Modern Design**: Beautiful, responsive design with gold/black/white color scheme
- **Automatic Image Slideshow**: 5-image hero slideshow with smooth transitions
- **Registration Form**: Comprehensive form with validation for required and optional fields
- **Google Sheets Integration**: Automatic data storage in Google Sheets
- **SMS Confirmation**: Automatic SMS confirmation via Twilio
- **Privacy Compliant**: Built-in privacy notice and consent mechanism
- **Responsive**: Works perfectly on mobile, tablet, and desktop
- **Real-time Validation**: Client-side form validation with helpful error messages
- **Rate Limiting**: Built-in protection against spam submissions

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**
- **UV** (Python package manager)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Google Account** (for Google Sheets API)
- **Twilio Account** (for SMS service) - Optional but recommended

## 🚀 Quick Start

### 1. Navigate to the Project

```bash
cd /home/christassaah/Desktop/Projects/iyc-registration-form
```

### 2. Set Up Virtual Environment

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

See the [Configuration](#-configuration) section below for detailed setup instructions.

## 🔧 Configuration

### Step 1: Google Sheets API Setup

This is **required** for the application to work.

#### 1.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select an existing project
3. Give your project a name (e.g., "IYC Conference Registration")
4. Click "Create"

#### 1.2 Enable Google Sheets API

1. In your project, go to **APIs & Services** > **Library**
2. Search for "Google Sheets API"
3. Click on it and press **Enable**

#### 1.3 Create Service Account

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **Service Account**
3. Enter service account details:
   - Name: `conference-registration`
   - Description: "Service account for conference registration"
4. Click **Create and Continue**
5. Skip the optional steps and click **Done**

#### 1.4 Create and Download Credentials

1. Click on the service account you just created
2. Go to the **Keys** tab
3. Click **Add Key** > **Create New Key**
4. Select **JSON** format
5. Click **Create**
6. The credentials file will download automatically
7. **Rename** the file to `credentials.json`
8. **Move** it to the project root directory:
   ```bash
   mv ~/Downloads/your-credentials-file.json /home/christassaah/Desktop/Projects/iyc-registration-form/credentials.json
   ```

#### 1.5 Create Your Google Sheet

1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new spreadsheet
3. Name it "IYC Conference Registrations" (or your preference)
4. Copy the **Sheet ID** from the URL:
   - URL format: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
   - Copy the `YOUR_SHEET_ID` part

#### 1.6 Share Sheet with Service Account

1. Open your Google Sheet
2. Click the **Share** button (top right)
3. In the credentials JSON file you downloaded, find the `client_email` field
   - It looks like: `conference-registration@project-id.iam.gserviceaccount.com`
4. **Paste this email** in the share dialog
5. Give it **Editor** permissions
6. **Uncheck** "Notify people"
7. Click **Share**

> ⚠️ **Important**: If you don't share the sheet with the service account, the application will not be able to save registrations!

### Step 2: Twilio SMS Setup

This is **optional** but highly recommended for SMS confirmations.

#### 2.1 Create Twilio Account

1. Go to [Twilio](https://www.twilio.com/try-twilio)
2. Sign up for a free trial account
3. Verify your phone number
4. You'll get **$15 free credit**

#### 2.2 Get Your Credentials

1. Go to the [Twilio Console](https://console.twilio.com/)
2. Find your **Account SID** and **Auth Token** on the dashboard
3. Copy these values

#### 2.3 Get a Phone Number

1. In the Twilio Console, go to **Phone Numbers** > **Manage** > **Buy a number**
2. Select a number (free with trial account)
3. Copy your Twilio phone number (format: +1234567890)

> 💡 **Alternative**: For Ghana-specific SMS, consider [Africa's Talking](https://africastalking.com/) which has better rates for African countries.

### Step 3: Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your actual values:
   ```bash
   nano .env
   ```

3. Fill in all the required values:

```env
# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
GOOGLE_SHEET_ID=your_actual_sheet_id_here

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Application Configuration
SECRET_KEY=your_secret_key_here_generate_with_openssl
CONFERENCE_NAME=IYC Conference 2024

# Links
WHATSAPP_GROUP_LINK=https://chat.whatsapp.com/your_invite_link
FACEBOOK_URL=https://facebook.com/your_page
YOUTUBE_URL=https://youtube.com/@your_channel

# Frontend URL
FRONTEND_URL=http://localhost:8000
```

4. Generate a secret key:
   ```bash
   openssl rand -hex 32
   ```
   Copy the output and paste it as your `SECRET_KEY`

## 🏃 Running Locally

### Option 1: Using the Startup Script (Recommended)

#### Development Mode (with hot-reload)
```bash
./start-dev.sh
```

#### Production Mode
```bash
./start.sh
```

### Option 2: Manual Start

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access the Application

1. Open your web browser
2. Navigate to: **`http://localhost:8000`**
3. You should see the beautiful registration page!

**The application serves both:**
- ✅ **Frontend**: `http://localhost:8000` (HTML, CSS, JS)
- ✅ **Backend API**: `http://localhost:8000/api/*`
- ✅ **API Documentation**: `http://localhost:8000/docs`

### Test the Health Check

Open another terminal and run:
```bash
curl http://localhost:8000/api/health
```

You should see a JSON response showing the status of all services.

## 🖼️ Customizing Images

### Replace Slideshow Images

1. Prepare 5 images for your slideshow (recommended size: 1200x600px or similar aspect ratio)
2. Name them: `slide1.jpg`, `slide2.jpg`, etc.
3. Replace the placeholder images in: `frontend/assets/images/slideshow/`
4. Supported formats: JPG, PNG, WebP

### Replace Logo

1. Prepare your organization logo (recommended size: 200x80px, PNG with transparent background)
2. Replace: `frontend/assets/images/logo.png`

## 📱 Testing the Application

### Manual Testing Checklist

- [ ] Slideshow automatically transitions every 5 seconds
- [ ] Previous/Next buttons work correctly
- [ ] Dot indicators show current slide
- [ ] Form validates required fields (Full Name, Phone, Church, City, Leader)
- [ ] Phone number accepts Ghana format (0XXXXXXXXX or +233XXXXXXXXX)
- [ ] Email validation works (when provided)
- [ ] Privacy consent checkbox is required
- [ ] Form shows loading state during submission
- [ ] Registration appears in Google Sheets after submission
- [ ] SMS confirmation is received (if Twilio configured)
- [ ] Thank you page displays with correct name
- [ ] WhatsApp link works on thank you page
- [ ] Social media links work
- [ ] Responsive design works on mobile
- [ ] "Register Another Person" link returns to registration page

### Test Form Submission

1. Fill out the form with test data
2. Use your actual phone number to test SMS
3. Check your Google Sheet for the new entry
4. Verify SMS confirmation was received

## 🚢 Deployment

### Deploy to Render.com (Free Tier)

#### 1. Prepare Your Repository

1. Initialize git (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Push to GitHub:
   ```bash
   git remote add origin YOUR_GITHUB_REPO_URL
   git branch -M main
   git push -u origin main
   ```

#### 2. Create Render Account

1. Go to [Render.com](https://render.com/)
2. Sign up with your GitHub account

#### 3. Create New Web Service

1. Click **New** > **Web Service**
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `iyc-conference-registration`
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

#### 4. Add Environment Variables

In the Render dashboard, go to **Environment** and add all variables from your `.env` file:

- `GOOGLE_SHEETS_CREDENTIALS_PATH`
- `GOOGLE_SHEET_ID`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `SECRET_KEY`
- `CONFERENCE_NAME`
- `WHATSAPP_GROUP_LINK`
- `FACEBOOK_URL`
- `YOUTUBE_URL`
- `FRONTEND_URL` (update to your Render URL, e.g., `https://your-app.onrender.com`)

#### 5. Upload Credentials File

For the Google credentials JSON:

1. In Render, go to **Secret Files**
2. Click **Add Secret File**
3. Filename: `credentials.json`
4. Paste the entire contents of your credentials JSON file
5. Save

#### 6. Deploy

1. Click **Create Web Service**
2. Render will automatically build and deploy your application
3. Once deployed, you'll get a URL like: `https://iyc-conference-registration.onrender.com`

#### 7. Update Frontend URL

The frontend is configured to use relative paths, so it will automatically work with your deployed URL. Just update the `FRONTEND_URL` environment variable in Render to match your deployment URL:

```
FRONTEND_URL=https://your-app.onrender.com
```

> ⚠️ **Free Tier Limitation**: The app will sleep after 15 minutes of inactivity and take ~30 seconds to wake up on the next request.

### Alternative: Deploy to Railway.app

Railway offers a similar free tier. Follow [Railway's Python deployment guide](https://docs.railway.app/guides/python).

## 🔒 Security Best Practices

- ✅ Never commit `.env` file or `credentials.json` to git
- ✅ Keep your Twilio credentials private
- ✅ Regularly rotate your `SECRET_KEY`
- ✅ Use HTTPS in production (Render/Railway provide this automatically)
- ✅ Review rate limiting settings if experiencing abuse
- ✅ Regularly backup your Google Sheet data
- ✅ Only share Google Sheet with necessary service accounts

## 🐛 Troubleshooting

### "Google Sheets authentication failed"

**Solution**:
1. Check that `credentials.json` exists in the correct location
2. Verify the sheet is shared with the service account email
3. Ensure Google Sheets API is enabled in your Google Cloud project

### "Twilio error: Unable to create record"

**Possible causes**:
- Twilio trial account requires verified phone numbers
- Incorrect Twilio credentials
- Phone number format issue

**Solution**:
1. Verify phone numbers in your Twilio console for trial accounts
2. Check `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`
3. Ensure phone number is in international format (+233...)

### "Rate limit exceeded"

**Solution**:
- Wait 1 minute and try again
- The app limits to 5 submissions per minute per IP to prevent spam

### Slideshow images not showing

**Solution**:
1. Check that images exist in `frontend/assets/images/slideshow/`
2. Verify file permissions: `chmod 644 frontend/assets/images/slideshow/*`
3. Check browser console for 404 errors

### Form submission fails

**Solution**:
1. Check backend is running: `curl http://localhost:8000/api/health`
2. Open browser developer console (F12) and check for errors
3. Verify `CONFIG.apiUrl` in `scripts/app.js` matches your backend URL

## 📊 Google Sheets Data Structure

Your Google Sheet will automatically create these columns:

| Timestamp | Full Name | Phone | Church | City/Location | Leader/Inviter | Email | Contact Method | First-Time Attendee | Prayer Request | Status |
|-----------|-----------|-------|--------|---------------|----------------|-------|----------------|---------------------|----------------|--------|

## 💰 Cost Breakdown

| Service | Free Tier | After Free Tier |
|---------|-----------|-----------------|
| Google Sheets API | ✅ Free (300 requests/min) | ✅ Still free |
| Twilio SMS | $15 trial credit (~1,900 SMS) | ~$0.0079 per SMS |
| Render.com Hosting | ✅ Free (with sleep) | $7/month (always on) |

## 📝 License

This project is provided as-is for the IYC Conference. Feel free to modify and customize it for your needs.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the terminal/console logs for error messages
3. Verify all environment variables are set correctly
4. Ensure all prerequisites are installed

## 🎉 Credits

Built with:
- **FastAPI** - Modern Python web framework
- **Google Sheets API** - Data storage
- **Twilio** - SMS service
- **UV** - Fast Python package manager
- **Vanilla JavaScript** - Client-side functionality

---

**May your conference registration be smooth and successful! God bless! 🙏**
