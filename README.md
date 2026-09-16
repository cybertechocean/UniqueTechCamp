# UniqueTechCamp (UTC)
### *Website, Clients, Income — High-Performance Web Applications & AI Customer Acquisition Systems*

[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![MariaDB](https://img.shields.io/badge/MariaDB-utf8mb4-003545?style=for-the-badge&logo=mariadb&logoColor=white)](https://mariadb.org/)
[![SEO Score](https://img.shields.io/badge/SEO-100%25_Optimized-22C55E?style=for-the-badge&logo=google&logoColor=white)](#seo--ai-search-optimization)
[![AI Ready](https://img.shields.io/badge/AI_Bots-Gemini_|_GPT_|_Claude-8B5CF6?style=for-the-badge&logo=openai&logoColor=white)](#ai-bots--crawlers-indexing)

---

## 🌟 Executive Overview

**UniqueTechCamp Limited** ([UniqueTechCamp.org](https://uniquetechcamp.org)) is an elite digital engineering firm based in Nairobi, Kenya. 

We do not sell static/generic "brochure" websites. We build **complete business growth engines** that combine custom, ultra-fast web applications with **24/7 AI Lead Generation, WhatsApp Lead Qualification, and Automated Multi-Channel Follow-up**. 

Every digital property we construct is engineered to turn casual website visitors into confirmed consultations, bookings, and revenue on autopilot.

---

## 🚀 Key Highlights & Architecture

### 1. 107 Industry Services with Embedded AI Growth Engines
- **107 pre-seeded niche services across 16 commercial categories** (Healthcare, Legal, Real Estate, E-Commerce, Hospitality, Education, Professional Services, etc.).
- Every service offering explicitly bundles:
  - High-converting modern web application architecture.
  - **24/7 AI WhatsApp Qualification Bot** (pre-screens leads based on budget, location, and urgency).
  - **Automated CRM & Lead Sync** (instant WhatsApp and email notifications to business owners).
  - **Omnichannel Follow-Up Funnels** (re-engages abandoned visitors).

### 2. High-Precision SEO & 100% Search Engine Optimization
- **Full Schema.org JSON-LD Graphs**:
  - `Organization` with complete Nairobi, Kenya geolocation, corporate social graph, and legal entity details.
  - `WebSite` with integrated Google `SearchAction` typeahead deep-link query spec.
  - `Service` schema with categorized deliverables and AI features on all 107 service detail pages.
  - `BlogPosting` and `BreadcrumbList` on all article pages.
- **Auto-Generated XML Sitemap**: Indexes 137+ live URLs at `/sitemap.xml` with dynamic change frequencies and priority weighting.
- **Syndication Feeds**:
  - RSS 2.0 Feed (`/feed/rss/`)
  - Atom 1.0 Feed (`/feed/atom/`)
  - Services Catalog Feed (`/feed/services/`)

### 3. AI Platform Indexing (`robots.txt` & `llms.txt`)
- **Explicit indexing for all major AI search crawlers**:
  - `Google-Extended` (Gemini / Google AI Overviews)
  - `GPTBot` & `ChatGPT-User` (OpenAI / ChatGPT Search)
  - `ClaudeBot` & `anthropic-ai` (Anthropic Claude)
  - `PerplexityBot` (Perplexity AI)
  - `Applebot-Extended` (Apple Intelligence)
  - `Cohere-ai`, `CCBot`, `FacebookBot`
- **Native LLM Documentation Endpoint**:
  - `/llms.txt` — Structured overview for AI agent discovery.
  - `/llms-full.txt` — Complete contextual digest of services and company competencies.

### 4. User Experience & Mobile First Design
- **Sticky Mobile Bottom Action Bar**: Mobile-only (`block md:hidden`) quick-action bar with 3 equal-width buttons (Services, Call, WhatsApp) and iOS safe-area support.
- **Floating Expandable Social Stack**: Fixed bottom-right widget expanding into 9 direct contact channels (Phone, WhatsApp, Email, TikTok, Facebook, Instagram, X, LinkedIn, YouTube).
- **Strict Icon Hygiene**: FontAwesome 6.6.0 strictly for social media brand logos; Lucide icons for all UI elements.
- **Global Instant Typeahead Search**: Live AJAX endpoint (`/api/search/`) with keyboard navigation and instant results across Services, Blog, Portfolio, and Policy pages.
- **Full Legal Suite**: Comprehensive GDPR and Kenya Data Protection Act 2019 compliant Privacy Policy, Terms of Service, Cookie Policy, and Payment Policy.

### 5. Content Management & Admin Studio
- **Django Unfold**: Premium, responsive dark/light admin interface styled in UniqueTechCamp's signature emerald palette (`#22c55e`, `#16a34a`, `#111827`).
- **Django CKEditor 5**: Full rich-text WYSIWYG editor for publishing SEO-optimized articles, code snippets, and case studies.

### 6. Internationalization & Database
- **Language**: `en-gb` (UK English).
- **Time Zone**: `Africa/Nairobi` (EAT, UTC+3).
- **Database**: MariaDB / MySQL configured with `utf8mb4` charset and `collation_connection=utf8mb4_unicode_ci` for full emoji support (🛒, 🏥, 🤖, etc.).
- **Caching**: Production database caching via `utc_cache_table`.

### 7. Branded Email Ecosystem (Welcome & Password Reset)
- **Top Brand Logo**: Official rounded logo (`logo-rounded.png`) prominently featured with emerald border.
- **Bottom Social Icons**: 9 bulletproof, email-client-compatible channel badges (WhatsApp, Phone, Email, TikTok, Facebook, Instagram, X, LinkedIn, YouTube) with direct links and Nairobi, Kenya headquarters metadata.
- **Automated Dispatches**:
  - `core.signals`: Automated welcome email dispatch whenever a new user account is created.
  - Standard Django `PasswordResetView`: Custom HTML email template (`templates/registration/password_reset_email.html`) and responsive web pages (`/auth/password_reset/`).
- **Live In-Browser Visual Previews**:
  - Welcome Email Preview: `/emails/preview/welcome/`
  - Password Reset Email Preview: `/emails/preview/password-reset/`
- **CLI Testing Utility**:
  - `python manage.py send_test_email --type=all --console` (instantly test and render emails in the terminal or send via SMTP).

---

## 📂 Project Structure

```text
UniqueTechCamp_Web/
├── manage.py                     # Django management script
├── passenger_wsgi.py             # cPanel / CloudLinux Passenger entrypoint
├── requirements.txt              # Production Python dependencies
├── .env.example                  # Environment variable reference
├── .gitignore                    # Git exclusion rules
│
├── uniquetechcamp/               # Core Project Configuration
│   ├── __init__.py               # PyMySQL as MySQLdb initialization
│   ├── settings.py               # Production settings (UK English, Nairobi TZ, Unfold, MariaDB)
│   ├── urls.py                   # Master routing (Sitemaps, Feeds, Robots, LLMs, Apps)
│   └── wsgi.py                   # WSGI application hook
│
├── core/                         # Base App, Search, Feeds, Sitemaps, Policies
│   ├── feeds.py                  # RSS 2.0 and Atom 1.0 feed generators
│   ├── sitemaps.py               # Dynamic XML sitemap generator (137+ URLs)
│   ├── urls.py                   # Search & policy endpoints
│   └── views.py                  # Home, About, Contact, Search, Robots, LLMs
│
├── services/                     # 107 Industry Services & Growth Systems
│   ├── models.py                 # ServiceCategory & Service models
│   ├── admin.py                  # Unfold ModelAdmin with filters & search
│   ├── urls.py                   # Service list and detail routes
│   ├── views.py                  # Category filtering and service views
│   └── management/commands/
│       └── seed_services.py      # Automated seeding of 107 services
│
├── blog/                         # Strategy & Thought Leadership Blog
│   ├── models.py                 # BlogCategory & Post (CKEditor 5 fields)
│   ├── admin.py                  # Unfold ModelAdmin with status toggles
│   ├── urls.py                   # Blog listing and slug detail routes
│   ├── views.py                  # Article views and related posts logic
│   └── management/commands/
│       └── seed_blog.py          # Seeding of initial growth articles
│
├── portfolio/                    # Showcase Projects & Case Studies
│   ├── models.py                 # Project models
│   ├── admin.py                  # Unfold admin registration
│   └── urls.py                   # Case study views
│
├── static/                       # Static Assets
│   ├── favicon.ico               # Multi-resolution ICO (16x16, 32x32, 48x48)
│   ├── favicon-16x16.png         # Crisp 16px favicon
│   ├── favicon-32x32.png         # Crisp 32px favicon
│   ├── apple-touch-icon.png      # 180x180 Apple touch icon
│   ├── android-chrome-192x192.png# Web manifest icon
│   ├── android-chrome-512x512.png# Web manifest icon
│   ├── site.webmanifest          # PWA Web Manifest
│   ├── images/
│   │   ├── logo-rounded.png      # High-res rounded company logo
│   │   └── logo-icon.png         # Rounded favicon badge
│   └── css/                      # Custom CSS utilities
│
├── staticfiles/                  # Collected static files (post collectstatic)
├── media/                        # User and admin uploaded media files
├── templates/                    # Django HTML5 Templates
│   ├── base.html                 # Master template with action bar, social stack, SEO
│   ├── 404.html                  # Branded 404 error page with search
│   ├── 500.html                  # Branded 500 server error page
│   ├── 403.html                  # Branded 403 forbidden error page
│   ├── emails/                   # Responsive HTML & Text email templates (Logo & Social)
│   │   ├── base_email.html       # Email wrapper with top logo & bottom 9 social links
│   │   ├── welcome_email.html    # Branded welcome email template
│   │   └── welcome_email.txt     # Plain text welcome email fallback
│   ├── registration/             # Authentication & Password Reset UI + Emails
│   │   ├── password_reset_email.html # Branded password reset HTML email
│   │   ├── password_reset_email.txt  # Plain text password reset email
│   │   ├── password_reset_form.html  # Password reset request page
│   │   ├── password_reset_done.html  # Reset link sent confirmation page
│   │   ├── password_reset_confirm.html# New password input page
│   │   └── password_reset_complete.html# Password reset success page
│   ├── pages/                    # Privacy, Terms, Cookie, Payment policies
│   ├── services/                 # Services catalogue & detail templates
│   ├── blog/                     # Blog listing and detail templates
│   └── search/                   # Full-text search results template
│
└── theme/                        # Tailwind CSS Theme Application
```

---

## 💻 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/cybertechocean/UniqueTechCamp.git
cd UniqueTechCamp
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create Local `.env` File
Create a `.env` file in the project root:
```env
SECRET_KEY=local-dev-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,uniquetechcamp.org
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create Database Cache Table
```bash
python manage.py createcachetable
```

### 7. Seed Database (107 Services + Blog Articles)
```bash
python manage.py seed_services
python manage.py seed_blog
```

### 8. Create Superuser (Admin Access)
```bash
python manage.py createsuperuser
```

### 9. Run the Local Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser. Admin portal is at `http://127.0.0.1:8000/admin/`.

---

## 🌐 Complete Shared Hosting Deployment Guide (cPanel)

This section provides the exact step-by-step procedure for deploying UniqueTechCamp to a shared hosting environment (cPanel / CloudLinux with Python Selector).

### Target Deployment Specifications
| Parameter | Value |
|---|---|
| **Domain** | `uniquetechcamp.org` / `www.uniquetechcamp.org` |
| **Document Root** | `/home2/genzcons/uniquetechcamp` |
| **Database Engine** | MariaDB 10.x+ (with `utf8mb4` support) |
| **Database Name** | `uniquetechcamp_db` |
| **Database User** | `uniquetechcamp_user` |
| **GitHub Repository** | `https://github.com/cybertechocean/UniqueTechCamp` |
| **Python Version** | Python 3.11 or 3.12 (via cPanel Python Selector) |

---

### Step 1: Create the MariaDB Database in cPanel
1. Log into your cPanel dashboard at your hosting provider.
2. Navigate to **Databases** > **MySQL Databases**.
3. Under **Create New Database**, enter:
   - Database Name: `uniquetechcamp_db` (or prefix `genzcons_uniquetechcamp_db`).
   - Click **Create Database**.
4. Under **Add New User**, enter:
   - Username: `uniquetechcamp_user`
   - Password: Click **Password Generator** to generate a strong password (e.g. `StrongP@ssw0rd2026!`). **Save this password!**
   - Click **Create User**.
5. Under **Add User To Database**:
   - Select User: `uniquetechcamp_user`
   - Select Database: `uniquetechcamp_db`
   - Click **Add**.
   - Check **ALL PRIVILEGES** and click **Make Changes**.

> [!TIP]
> Our database configuration automatically executes:
> `SET default_storage_engine=INNODB, character_set_connection=utf8mb4, collation_connection=utf8mb4_unicode_ci`
> on every connection, ensuring that emojis (🛒, 🏥, 🤖) are saved properly without database collation errors.

---

### Step 2: Setup Python Application in cPanel
1. In cPanel, scroll to the **Software** section and click **Setup Python App**.
2. Click **Create Application**.
3. Fill in the parameters:
   - **Python version**: Select **3.11** or **3.12**.
   - **Application root**: `uniquetechcamp` (this points to `/home2/genzcons/uniquetechcamp`).
   - **Application URL**: Select `uniquetechcamp.org`.
   - **Application startup file**: `passenger_wsgi.py`.
   - **Application Entry point**: `application`.
4. Click **Create** in the upper right corner.
5. Once created, cPanel will display a command to enter the virtual environment at the top of the page. It will look like:
   ```bash
   source /home2/genzcons/virtualenv/uniquetechcamp/3.12/bin/activate && cd /home2/genzcons/uniquetechcamp
   ```
   **Copy this command for terminal use.**

---

### Step 3: Clone Code from GitHub via SSH / Terminal
1. In cPanel, open the **Terminal** tool (under **Advanced**).
2. If the directory `/home2/genzcons/uniquetechcamp` already has default files created by cPanel, back them up or clear the directory:
   ```bash
   cd /home2/genzcons
   rm -rf uniquetechcamp
   git clone https://github.com/cybertechocean/UniqueTechCamp.git uniquetechcamp
   cd uniquetechcamp
   ```

---

### Step 4: Configure Production `.env` File
In `/home2/genzcons/uniquetechcamp`, create your production `.env` file using the nano editor:
```bash
nano .env
```
Paste and customize the following production configuration:
```env
# Core Django Security
SECRET_KEY=paste_a_secure_50_character_random_string_here
DEBUG=False
ALLOWED_HOSTS=uniquetechcamp.org,www.uniquetechcamp.org,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://uniquetechcamp.org,https://www.uniquetechcamp.org
SECURE_SSL_REDIRECT=True

# MariaDB / MySQL Configuration (with utf8mb4 full emoji support)
DB_ENGINE=django.db.backends.mysql
DB_NAME=genzcons_uniquetechcamp_db
DB_USER=genzcons_uniquetechcamp_user
DB_PASSWORD=YourStrongDatabasePasswordHere
DB_HOST=localhost
DB_PORT=3306

# SMTP Email Configuration (Google App Password)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=UniqueTechCamp@gmail.com
EMAIL_HOST_PASSWORD=your_16_character_app_password
DEFAULT_FROM_EMAIL=UniqueTechCamp Web Developers <info@uniquetechcamp.org>
SERVER_EMAIL=UniqueTechCamp Web Developers <info@uniquetechcamp.org>
```
Press `Ctrl+O` then `Enter` to save, and `Ctrl+X` to exit nano.

---

### Step 5: Activate Virtualenv & Install Requirements
In the cPanel Terminal, activate the Python environment and install all packages:
```bash
# Activate virtual environment (use your exact cPanel path)
source /home2/genzcons/virtualenv/uniquetechcamp/3.12/bin/activate

# Move to the application directory
cd /home2/genzcons/uniquetechcamp

# Upgrade pip
pip install --upgrade pip

# Install all production dependencies
pip install -r requirements.txt
```

---

### Step 6: Run Database Migrations
Execute Django's migrations to generate all database tables in MariaDB:
```bash
python manage.py migrate
```

---

### Step 7: Create the Database Cache Table
Create the database cache table `utc_cache_table` for high-speed page and query caching:
```bash
python manage.py createcachetable
```

---

### Step 8: Seed 107 Services & Initial Blog Articles
Populate the database with the full catalog of 107 industry services and thought leadership blog posts:
```bash
# Seed all 107 industry services and categories
python manage.py seed_services

# Seed the initial blog articles
python manage.py seed_blog
```

---

### Step 9: Create Django Admin Superuser
Create your administrator account for the Unfold Management Studio:
```bash
python manage.py createsuperuser
```
Follow the prompts to set your username, email (`info@uniquetechcamp.org`), and strong password.

---

### Step 10: Collect Static Files
Collect and compress all CSS, JS, favicons, logos, and CKEditor static assets into `staticfiles/` via WhiteNoise:
```bash
python manage.py collectstatic --noinput
```

---

### Step 11: Configure `passenger_wsgi.py` & Restart Application
Confirm `passenger_wsgi.py` exists in `/home2/genzcons/uniquetechcamp/passenger_wsgi.py`. The repository includes the production file:
```python
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

try:
    from dotenv import load_dotenv
    env_path = os.path.join(PROJECT_DIR, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniquetechcamp.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

To restart the application on cPanel Passenger:
```bash
# Method A: Touch the restart file
mkdir -p /home2/genzcons/uniquetechcamp/tmp
touch /home2/genzcons/uniquetechcamp/tmp/restart.txt

# Method B: In cPanel "Setup Python App", click the "Restart" button for uniquetechcamp.org
```

---

### Step 12: Verify SSL and Endpoints
1. Ensure **AutoSSL** or **Let's Encrypt** SSL is active for `uniquetechcamp.org` in cPanel **SSL/TLS Status**.
2. Visit the live endpoints in your web browser:
   - Homepage: `https://uniquetechcamp.org/`
   - Services Catalog: `https://uniquetechcamp.org/services/`
   - Blog: `https://uniquetechcamp.org/blog/`
   - XML Sitemap: `https://uniquetechcamp.org/sitemap.xml` (verifies 137+ indexed URLs)
   - RSS Feed: `https://uniquetechcamp.org/feed/rss/`
   - Atom Feed: `https://uniquetechcamp.org/feed/atom/`
   - Robots: `https://uniquetechcamp.org/robots.txt`
   - LLMs Spec: `https://uniquetechcamp.org/llms.txt`
   - Unfold Admin: `https://uniquetechcamp.org/admin/`

---

## 🛠️ Ongoing Maintenance & Updates

### Pulling Updates from GitHub
Whenever you push updates to GitHub, pull them to production in 3 commands:
```bash
source /home2/genzcons/virtualenv/uniquetechcamp/3.12/bin/activate
cd /home2/genzcons/uniquetechcamp
git pull origin main
python manage.py migrate
python manage.py collectstatic --noinput
touch tmp/restart.txt
```

### Inspecting Error Logs
If an unexpected error occurs:
```bash
# View Passenger execution log
cat /home2/genzcons/uniquetechcamp/passenger.log

# View cPanel error logs
cat /home2/genzcons/logs/uniquetechcamp.org-error_log
```

---

## 📜 Intellectual Property & Licensing

Copyright &copy; 2026 **UniqueTechCamp Limited**. All rights reserved.  
*Engineered in Nairobi, Kenya.*
