# Ka-tch Mail - Email Service Case Study

---

## 🤖 AI-POWERED EMAIL SUMMARIZER (Headline Feature)

<div align="center">

### ✨ Powered by Google Gemini AI ✨

</div>

One of the standout features of this redesign is the **AI Email Summarizer** - an intelligent assistant that analyzes your entire inbox and generates comprehensive summaries with a single click.

### How It Works:
1. Click the **"🤖 AI Summarize"** button in the sidebar
2. A beautiful modal appears asking if you want to summarize your emails
3. Click **"Generate Summary"** and watch the AI analyze your inbox
4. Receive a structured report with:
   - 📊 **Overview** - Inbox status and key statistics
   - 🔥 **Key Highlights** - Most important/urgent emails
   - 📋 **Action Items** - Tasks extracted from emails
   - 👥 **Key Contacts** - Main people and message context
   - 💡 **Insights** - Patterns and observations

### Technical Implementation:
- **API**: Google Gemini 1.5 Flash
- **Integration**: Client-side JavaScript with async/await
- **UI**: Custom modal with loading states and formatted output
- **Error Handling**: Toast notifications for failures

```javascript
// Example: AI Summary Request
const response = await fetch(`${GEMINI_API_URL}?key=${API_KEY}`, {
  method: 'POST',
  body: JSON.stringify({
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: { temperature: 0.7, maxOutputTokens: 2048 }
  })
});
```

---

## 🎨 Design Inspiration & Credits

The UI design for this project was inspired by the clean, modern aesthetics of:
- **[RealDoc.app](https://realdoc.app/)** - Professional SaaS design with gradient backgrounds and card-based layouts
- **[ScrubsAndMore.us](https://www.scrubsandmore.us/)** - Warm, customer-focused design with excellent visual hierarchy

The **UX (User Experience)** is an original design focused on:
- **Intuitive navigation** with a persistent sidebar for quick access
- **Visual feedback** through toast notifications, loading states, and animations
- **Progressive disclosure** - showing email previews in list, full content on click
- **Real-time password validation** to guide users during registration
- **Contextual actions** - star, delete, reply directly from email view

---

## Overview

Ka-tch Mail is a modern email service case study featuring a Flask backend and a completely redesigned, creative HTML/CSS/JS frontend. The design intentionally avoids conventional email client patterns (Gmail, Outlook) in favor of a unique, visually striking interface.

---

## ✨ Features

### Original Features
- User registration with password rules (uppercase, lowercase, number, special symbol, confirmation)
- Auto-generated user email addresses (`<username>@ka-tch.com`)
- Registration fields: first name, last name, date of birth
- User login/logout
- Send email (Flask-Mail integration, demo mode)
- View dummy inbox (with edge-case data, labels for sent/inbox)
- Session-based authentication

### 🆕 New Frontend Features
- **Modern Dark Theme** - Sleek purple gradient accents on dark background
- **Animated UI** - Smooth transitions, hover effects, and loading skeletons
- **Real-time Password Validation** - Visual checklist for password requirements
- **Toast Notifications** - Success/error feedback for all actions
- **Email Search** - Filter emails by subject, body, or sender
- **Email Filtering** - View Inbox, Sent, Starred, or All Mail
- **Starred Emails** - Mark important emails for quick access
- **Read/Unread Status** - Visual indicators for new messages
- **Email Detail View** - Full email view with reply functionality
- **Responsive Design** - Works on desktop and mobile devices
- **Keyboard Shortcuts** - Escape to close modals

### 🆕 Bonus Backend Features (API Enhancements)
- `GET /auth/profile` - Retrieve user profile information
- `GET /mail/inbox/count` - Get email counts (total, unread, inbox, sent, starred)
- `DELETE /mail/inbox/<id>` - Delete an email by ID
- `PUT /mail/inbox/<id>/read` - Toggle read/unread status
- `PUT /mail/inbox/<id>/star` - Toggle starred status

---

## Prerequisites
- Python 3.10+
- pip (Python package manager)

---

## Setup Instructions

### 1. Clone the Repository
```
git clone https://github.com/Ka-Technology/front-end-case-study-1.git
cd front-end-case-study-1
```

### 2. Set up virtual environment
#### Linux
```
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

#### Mac OS
```
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```
### Windows
```
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

```

### 3. Install Python Dependencies
```
cd backend
pip install -r requirements.txt
```

### 4. Run the Flask Backend
```
cd backend
python app.py
```
- The backend will start on `http://127.0.0.1:8080/` by default.


### 5. Run the Frontend (Optional: Using a Simple HTTP Server)
You can serve the frontend using a simple HTTP server so that it runs on a different port than the backend. This is recommended for local development.

#### Using Python (from the project root or `frontend/` folder):
```
cd frontend
python -m http.server 3000
```
- This will serve the frontend at `http://localhost:3000/`.
- Open your browser and go to `http://localhost:3000/` to use the app.

#### Alternative: Using Node.js (if installed)
```
npm install -g serve
cd frontend
serve -l 3000
```

- The frontend will interact with the backend via HTTP requests.
- **It is your job to design, develop, and connect the backend code for it!**

---

## File Structure
```
backend/
  app.py                # Main Flask app
  requirements.txt      # Python dependencies
  routes/
    auth_routes.py      # Auth endpoints (register, login, logout, status)
    mail_routes.py      # Mail endpoints (send, inbox, status)
frontend/
  index.html            # Simple HTML/JS frontend
```

---

## API Reference

### Authentication Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | POST | Register a new user |
| `/auth/login` | POST | Login with username/password |
| `/auth/logout` | POST | Logout current user |
| `/auth/status` | GET | Check authentication status |
| `/auth/profile` | GET | Get current user's profile (🆕 Bonus) |

### AI Features
| Feature | Description |
|---------|-------------|
| AI Email Summarizer | Uses Google Gemini AI to analyze and summarize all emails |
| Smart Insights | Extracts action items, key contacts, and highlights |
| One-Click Summary | Beautiful modal with structured AI-generated report |

### Mail Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mail/inbox` | GET | Get all emails |
| `/mail/send` | POST | Send a new email |
| `/mail/status` | GET | Check mail service status |
| `/mail/inbox/count` | GET | Get email counts (🆕 Bonus) |
| `/mail/inbox/<id>` | DELETE | Delete an email (🆕 Bonus) |
| `/mail/inbox/<id>/read` | PUT | Toggle read status (🆕 Bonus) |
| `/mail/inbox/<id>/star` | PUT | Toggle starred status (🆕 Bonus) |

---

## Notes
- All backend endpoints are documented with comments in the code.
- The dummy inbox is in-memory and resets on server restart.
- Password rules are enforced on registration.
- Email sending is simulated for demo/testing.
- The frontend uses vanilla HTML/CSS/JS with no external frameworks
- Design intentionally avoids Gmail/Outlook patterns for originality

---

## Screenshots & Features Gallery

The redesigned frontend features:
- 🤖 **AI Email Summarizer** - One-click inbox analysis powered by Gemini
- 🌙 Dark theme with purple gradient accents
- 📬 Card-based email list with dynamic avatars
- ✨ Feature showcase transition screen after login
- 🔐 Real-time password validation with visual checklist
- 📱 Responsive design for all screen sizes
- 🔔 Toast notifications for all actions
- ⭐ Star/unstar emails with persistent storage
- 🗑️ Delete emails with confirmation
- 🔍 Search and filter functionality

---

## Author
Ka Technology

Frontend Redesign & Backend Enhancements by: AI Assistant

---

## License
See `LICENSE` file.