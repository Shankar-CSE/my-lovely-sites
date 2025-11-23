# URL Organizer

A minimal Flask application to organize and manage URLs with a clean, modern dashboard.

## Features

- 📋 **Public URL Catalog** - Beautiful grid of organized URLs visible to everyone
- 🔐 **Admin Authentication** - Secure login for admin access
- ✏️ **CRUD Operations** - Create, read, update, and delete URLs
- 🏷️ **Tag System** - Organize URLs with tags and filter by them
- 🔍 **Search** - Find URLs quickly by title or description
- 📊 **Dashboard Stats** - See total URLs, tags, and filtered counts
- 🎨 **Modern UI** - Tailwind CSS with Google Fonts (Inter)

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: Jinja2 templates + Tailwind CSS (CDN) + Google Fonts
- **Authentication**: Session-based with argon2 password hashing

## Setup

### Prerequisites

- Python 3.8+
- MongoDB (local or Atlas)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd url-organizer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   - `MONGO_URI` - Your MongoDB connection string
   - `SECRET_KEY` - A random secret key for sessions
   - `ADMIN_USERNAME` - Your admin username
   - `ADMIN_PASSWORD_HASH` - Generate using the script below

5. **Generate admin password hash**
   ```bash
   python scripts/hash_password.py
   ```
   Copy the generated hash to `ADMIN_PASSWORD_HASH` in `.env`

6. **Run the application**
   ```bash
   python run.py
   ```
   
   The app will be available at `http://localhost:5000`

## Usage

### Public View
- Visit `http://localhost:5000` to see the organized URL catalog
- Click on any URL card to visit the link
- Filter by tags by clicking on tag badges

### Admin Access
1. Navigate to `http://localhost:5000/admin/login`
2. Login with your admin credentials
3. Access the dashboard at `http://localhost:5000/admin`
4. Add, edit, or delete URLs
5. Search and filter your URL collection

## Project Structure

```
url-organizer/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── db.py                # MongoDB connection
│   ├── repositories/
│   │   └── url_repo.py      # Database operations
│   ├── routes/
│   │   ├── public.py        # Public routes
│   │   ├── admin.py         # Admin routes
│   │   └── auth.py          # Authentication routes
│   ├── services/
│   │   ├── auth_service.py  # Auth logic
│   │   └── url_service.py   # URL business logic
│   └── templates/
│       ├── base.html        # Base template
│       ├── index.html       # Public catalog
│       ├── login.html       # Login page
│       ├── dashboard.html   # Admin dashboard
│       └── url_form.html    # Create/Edit form
├── scripts/
│   ├── hash_password.py     # Generate password hash
│   └── seed_data.py         # Seed sample data
├── .env.example             # Environment template
├── .gitignore
├── requirements.txt
├── run.py                   # Application entry point
└── README.md
```

## Optional: Seed Sample Data

```bash
python scripts/seed_data.py
```

This will add some sample URLs to get you started.

## Deployment

### Vercel (Recommended for Serverless)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Add environment variables in Vercel dashboard:
     - `MONGO_URI` - Your MongoDB Atlas connection string
     - `SECRET_KEY` - Generate a secure random string
     - `ADMIN_USERNAME` - Your admin username
     - `ADMIN_PASSWORD_HASH` - Generated hash from `scripts/hash_password.py`
     - `FLASK_ENV` - Set to `production`
   - Deploy!

3. **Important**: Whitelist Vercel's IP addresses in MongoDB Atlas Network Access

### Railway / Render / Fly.io

1. **Connect your repository** to the platform
2. **Set environment variables** (same as above)
3. **Deploy** - The platform will automatically detect the Dockerfile or use the Procfile

### Docker

```bash
# Build the image
docker build -t url-organizer .

# Run the container
docker run -p 8000:8000 \
  -e MONGO_URI="your_mongo_uri" \
  -e SECRET_KEY="your_secret" \
  -e ADMIN_USERNAME="admin" \
  -e ADMIN_PASSWORD_HASH="your_hash" \
  url-organizer
```

## Environment Variables

Required environment variables for production:

- `MONGO_URI` - MongoDB connection string (Atlas recommended)
- `SECRET_KEY` - Flask secret key (generate a random string)
- `ADMIN_USERNAME` - Admin username
- `ADMIN_PASSWORD_HASH` - Argon2 password hash
- `FLASK_ENV` - Set to `production`

## License

MIT
