# MiniMeet – Simple Meeting Scheduler

This is a lightweight Django app that allows visitors to book meetings with a boss, generates calendar files (`.ics`), and provides a simple dashboard for the boss to manage meetings, add comments, and sign off.

---

## Features
- **Meeting Booking Form**
  - Captures **Name, Organization, Reason, Date & Time**
  - Generates an **.ics calendar file** for the user
  - Provides a **Google Calendar link** option

- **Boss Dashboard**
  - Displays upcoming meetings
  - Boss can add **comments** after the meeting
  - Boss can add a **signature/approval**

- **Calendar Integration**
  - Downloadable **.ics file** for Outlook/Apple/Google Calendar
  - Easy “Add to Google Calendar” link

---

## Setup Instructions

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/minimeet.git
cd minimeet
pip install -r requirements.txt
```

### 2. Dependencies
- Django
- ics (for generating calendar files)

Install them:
```bash
pip install django ics
```

### 3. Run the Server
```bash
python manage.py migrate
python manage.py runserver
```

Access the app at: [http://localhost:8000](http://localhost:8000)

---

## Usage

### Book a Meeting
1. Go to `/book/`
2. Fill in **Name, Organization, Reason, Date/Time**
3. Submit → Download `.ics` file or click **Add to Google Calendar**

### Boss Dashboard
- Visit `/dashboard/` to see all meetings
- Click on a meeting → Add **comments and signature**

---

## Example Google Calendar Integration
To add a meeting directly to Google Calendar:
```text
https://calendar.google.com/calendar/render?action=TEMPLATE&text=Meeting+with+{Name}&dates={start}/{end}&details={Reason+for+Visit}&location={Organization}
```

Replace placeholders with meeting details.

---

## Next Steps / Improvements
- Add email notifications (send `.ics` file to user)
- Add Slack/WhatsApp notifications for boss
- Enable multi-user / role-based access
- Improve UI with Bootstrap/Tailwind
- Deploy to a server (Heroku, Vercel, or VPS)

---

## License
MIT License
