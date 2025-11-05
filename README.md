# AI-Automations-and-Scraping

A collection of automation and scraping projects demonstrating various AI-powered tools and workflows.

## 📁 Projects

### 1. LinkedIn Scraper (`/linkedin_scraper`)
A Python-based LinkedIn profile scraper with Selenium automation.

**Features:**
- Automated LinkedIn profile data extraction
- Chrome profile integration
- Configurable scraping parameters

[View LinkedIn Scraper README](linkedin_scraper/README.md)

---

### 2. Autodialer and Blog Generator (`/autodialer_and_blog_generator`)
A Ruby on Rails application for automated phone calling and AI blog generation.

**Features:**
- 📞 **Bulk Phone Calling**: Call up to 100 numbers automatically via Twilio
- 🤖 **AI Voice**: Natural-sounding voices using Amazon Polly Neural
- 💬 **Natural Language Commands**: "Call +18001234567" - AI extracts and executes
- 📊 **Call Analytics**: Track status, duration, success/failure rates
- ✍️ **AI Blog Generator**: Generate programming articles using Google Gemini 2.0 Flash
- 📝 **Bulk Content Creation**: Create up to 10 articles at once

**Tech Stack:**
- Ruby on Rails 8.1
- Twilio API (phone calls)
- Google Gemini 2.0 Flash API (content generation - FREE for developers)
- Bootstrap 5 (UI)
- PostgreSQL (database)

**Quick Start:**
```bash
cd autodialer
bundle install
rails db:create db:migrate
rails server
```

Visit `http://localhost:3000`

**Documentation:**
- [Main README](autodialer/README.md) - Setup and usage
- [Ruby Guide](autodialer/RUBY_GUIDE.md) - Ruby basics and how the app works
- [Deployment Guide](autodialer/DEPLOYMENT.md) - Deploy to Heroku/Render/Railway

**Environment Variables Required:**
```bash
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number
GEMINI_API_KEY=your_gemini_key
```

[View Autodialer Full Documentation](autodialer/README.md)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x (for LinkedIn Scraper)
- Ruby 3.4+ (for Autodialer)
- Git

### Clone Repository
```bash
git clone https://github.com/harshj3915/AI-Automations-and-Scraping.git
cd AI-Automations-and-Scraping
```

### Choose Your Project
Navigate to either project folder and follow its README:
- `cd linkedin_scraper` for Python scraping project
- `cd autodialer` for Ruby on Rails calling/blogging app

---

## 📊 Project Comparison

| Feature | LinkedIn Scraper | Autodialer |
|---------|-----------------|------------|
| Language | Python | Ruby |
| Framework | Selenium | Rails |
| Purpose | Data Scraping | Automation & Content |
| APIs Used | None | Twilio, Google Gemini |
| Database | None | PostgreSQL/SQLite |
| UI | CLI | Web Interface |
| Deployment | Local | Heroku/Render/Railway |

---

## 🎓 Learning Resources

### For LinkedIn Scraper:
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Python Web Scraping Guide](https://realpython.com/beautiful-soup-web-scraper-python/)

### For Autodialer:
- [Ruby Guide](autodialer/RUBY_GUIDE.md) - Comprehensive Ruby basics
- [Rails Guides](https://guides.rubyonrails.org/)
- [Twilio Documentation](https://www.twilio.com/docs)
- [Google Gemini API](https://ai.google.dev/docs)

---

## 🔐 Security Notes

- Never commit API keys or credentials
- Use `.env` files for sensitive data
- Add `.env` to `.gitignore`
- Use environment variables in production
- Regularly update dependencies

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Harsh Jain**
- GitHub: [@harshj3915](https://github.com/harshj3915)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⭐ Show Your Support

Give a ⭐️ if these projects helped you!

---

## 📧 Contact

For questions or feedback, please open an issue in the GitHub repository.
