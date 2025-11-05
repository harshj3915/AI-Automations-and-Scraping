# Autodialer - AI-Powered Phone Dialer & Blog Platform

A Ruby on Rails application that combines automated phone calling with AI-powered blog content generation. This application allows you to make bulk phone calls using Twilio's API with AI voices and generate programming blog posts using OpenAI's GPT models.

## 🌟 Features

### Phone Dialer
- **Bulk Phone Calling**: Call up to 100 numbers automatically
- **AI Voice Integration**: Uses Amazon Polly Neural voices for natural-sounding calls
- **Natural Language Commands**: Use AI to parse commands like "Call +18001234567"
- **Call Analytics**: Track call status, duration, success/failure rates
- **Multiple Input Methods**: Paste numbers, upload files, or use AI commands
- **Real-time Status Updates**: Twilio webhooks for live call status tracking

### Blog Platform
- **AI Content Generation**: Generate comprehensive blog posts using Google Gemini 2.0
- **Bulk Generation**: Create up to 10 articles at once
- **Programming Topics**: Specialized in technical and programming content
- **Customizable**: Add details to guide AI content generation
- **SEO-Friendly**: Auto-generated slugs and proper formatting

## 📋 Prerequisites

-  3.4+ installed
- Rails 8.1+ installed
- **PostgreSQL database** (SQLite3 has Ruby 3.4 compatibility issues on Windows)
- Twilio Account (for phone calls)
- Google Gemini API Key (for blog generation - FREE for developers)

## 🚀 Installation

### 1. Navigate to the Project

```bash
cd autodialer
```

### 2. Install Dependencies

```bash
bundle install
```

### 3. Configure Environment Variables

Add Twilio and Gemini credentials to `.env`:

```bash
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
```

#### Getting Twilio Credentials:
1. Sign up at [Twilio.com](https://www.twilio.com/try-twilio)
2. Get $15 free credit for testing
3. Go to Console Dashboard to find Account SID and Auth Token
4. Get a phone number from Phone Numbers → Buy a Number

#### Getting Google Gemini API Key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy the API key (starts with `AIzaSy...`)
5. **Note**: Gemini API is FREE for developers with generous rate limits!

### 4. Create and Migrate Database

```bash
rails db:create
rails db:migrate
```

**Note**: If you get connection errors, see [POSTGRES_SETUP.md](POSTGRES_SETUP.md) for troubleshooting.

### 5. Start the Server

```bash
rails server
```

Visit `http://localhost:3000` in your browser.

## 📱 Usage

### Making Phone Calls

**⚠️ Important**: As i am using Twilio trial account, only verified number only Twilio can be called.

#### Method 1: Bulk Upload
1. Navigate to "Phone Calls" → "Make New Calls"
2. Enter phone numbers (one per line) or upload a text file
3. Click "Start Auto-Dialing"

#### Method 2: AI Command
1. Go to "Phone Calls" page
2. Type: "Make a call to +18001234567"
3. Click "Execute AI Command"

### Generating Blog Posts

1. Navigate to "Blog" → "Generate New Posts with AI"
2. Enter blog post titles (one per line)
3. Format: `Title | Additional context` (context is optional)
4. Click "Generate Posts with AI"

## 📊 API Costs

- **Twilio**: $0.013-$0.04 per minute, $15 free trial credit
- **Google Gemini**: **FREE for developers** with 60 requests per minute rate limit
  - Gemini 2.0 Flash: Extremely fast and completely free
  - No credit card required for API key

## 🐛 Troubleshooting

### SQLite3 Issues
Switch to PostgreSQL in Gemfile if you encounter issues with Ruby 3.4:
```ruby
gem 'pg', '~> 1.5'
```

### Twilio Errors
- Verify account is active and has credit
- Check phone number format includes country code (+1)
- Ensure number is verified for trial accounts

### Gemini API Errors
- Verify API key is correct and active
- Check rate limits (60 requests/minute for free tier)
- Ensure proper JSON parsing in responses

## 📚 Additional Resources

- [Twilio Documentation](https://www.twilio.com/docs)
- [Google Gemini API Documentation](https://ai.google.dev/docs)

## 📄 License

Open source under MIT License.

---

**Note**: This is a demonstration application. Use responsibly and comply with Twilio's and OpenAI's terms of service.
