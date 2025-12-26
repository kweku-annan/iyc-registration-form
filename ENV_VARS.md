# Environment Variables for Backend (Render.com)

Copy these to your Render.com dashboard when setting up the web service:

## Required Variables

```
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json
GOOGLE_SHEET_ID=your_google_sheet_id_here
MNOTIFY_API_KEY=your_mnotify_api_key_here
SECRET_KEY=your_secret_key_here
CONFERENCE_NAME=IYC Conference 2025
WHATSAPP_GROUP_LINK=https://chat.whatsapp.com/your_link
FACEBOOK_URL=https://facebook.com/your_page
YOUTUBE_URL=https://youtube.com/@your_channel
FRONTEND_URL=https://your-frontend.vercel.app
```

## Secret Files

Upload `credentials.json` as a Secret File in Render:
- Filename: `credentials.json`
- Contents: Your Google Service Account JSON file

## How to Set in Render

1. Go to your service dashboard
2. Click "Environment" tab
3. Add each variable above
4. Save changes
5. Service will automatically redeploy
