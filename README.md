# Health Tech Ecosystem - Backend API

A comprehensive Flask-based backend API for the Health Tech Ecosystem, providing services for patient management, telemedicine, research data management, and AI integration.

## Features

- **Authentication & Authorization:** JWT-based authentication with role-based access control
- **Patient Management:** Complete patient records and medical history management
- **Healthcare Provider Management:** Provider profiles and specializations
- **Appointment Scheduling:** Appointment booking and management
- **Telemedicine:** Virtual consultation support with real-time messaging
- **Research Management:** Research project, dataset, and collaboration management
- **AI Integration:** OmniCognitor AI platform integration
- **Real-time Features:** WebSocket support for live updates
- **HIPAA Compliant:** Secure data handling and encryption

## Technology Stack

- **Framework:** Flask 3.0.0
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Authentication:** JWT (PyJWT)
- **Real-time:** Flask-SocketIO
- **API Documentation:** RESTful API design

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── user.py              # User and Profile models
│   │   ├── healthcare.py        # Patient, Provider, Appointment models
│   │   ├── telemed.py           # Teleconsultation, Message models
│   │   ├── research.py          # Research project models
│   │   ├── ai.py                # AI models
│   │   └── __init__.py
│   ├── routes/
│   │   ├── auth_routes.py       # Authentication endpoints
│   │   ├── healthcare_routes.py # Healthcare endpoints
│   │   ├── telemed_routes.py    # Telemedicine endpoints
│   │   ├── research_routes.py   # Research endpoints
│   │   ├── ai_routes.py         # AI endpoints
│   │   └── __init__.py
│   └── utils/
│       ├── auth.py              # Authentication utilities
│       └── __init__.py
├── app.py                       # Application factory
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip or poetry

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd backend
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize the database:**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Run the development server:**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh JWT token
- `POST /api/auth/logout` - Logout user

### Healthcare
- `GET /api/healthcare/patients` - List patients
- `POST /api/healthcare/patients` - Create patient
- `GET /api/healthcare/patients/<id>` - Get patient details
- `GET /api/healthcare/appointments` - List appointments
- `POST /api/healthcare/appointments` - Create appointment
- `PUT /api/healthcare/appointments/<id>` - Update appointment
- `GET /api/healthcare/medical-records` - Get medical records
- `POST /api/healthcare/medical-records` - Create medical record

### Telemedicine
- `GET /api/telemed/consultations` - List consultations
- `POST /api/telemed/consultations/<id>/start` - Start consultation
- `POST /api/telemed/consultations/<id>/end` - End consultation
- `GET /api/telemed/messages` - Get messages
- `POST /api/telemed/messages` - Send message

### Research
- `GET /api/research/projects` - List projects
- `POST /api/research/projects` - Create project
- `GET /api/research/projects/<id>` - Get project details
- `GET /api/research/projects/<id>/datasets` - List datasets
- `POST /api/research/projects/<id>/datasets` - Upload dataset
- `GET /api/research/projects/<id>/collaborations` - List collaborations
- `GET /api/research/projects/<id>/outputs` - Get outputs

### AI
- `GET /api/ai/models` - List AI models
- `GET /api/ai/models/<id>` - Get model details
- `GET /api/ai/agents` - List AI agents
- `POST /api/ai/agents` - Create agent
- `POST /api/ai/agents/<id>/interact` - Interact with agent
- `GET /api/ai/interactions` - Get user interactions

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/health_tech_db

# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# External Services
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-key
```

## Database Schema

### Users Table
- `id` - UUID primary key
- `email` - Unique email address
- `password_hash` - Hashed password
- `role` - User role (admin, healthcare_provider, patient, researcher, ai_admin)
- `is_active` - Account status
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Patients Table
- `id` - FK to users.id
- `ehr_id` - Electronic Health Record ID
- `medical_history` - JSON medical history
- `allergies` - Array of allergies
- `current_medications` - Array of medications
- `primary_care_provider_id` - FK to healthcare_providers

### Healthcare Providers Table
- `id` - FK to users.id
- `license_number` - Medical license number
- `specialization` - Medical specialization
- `clinic_address` - Clinic address
- `is_available` - Availability status

### Appointments Table
- `id` - UUID primary key
- `patient_id` - FK to patients.id
- `provider_id` - FK to healthcare_providers.id
- `start_time` - Appointment start time
- `end_time` - Appointment end time
- `appointment_type` - Type (telemedicine, in_person, follow_up)
- `status` - Status (scheduled, completed, cancelled)

### Medical Records Table
- `id` - UUID primary key
- `patient_id` - FK to patients.id
- `provider_id` - FK to healthcare_providers.id
- `diagnosis` - Diagnosis text
- `treatment` - Treatment text
- `prescription` - JSON prescription data
- `attachments` - Array of file URLs

### Research Projects Table
- `id` - UUID primary key
- `name` - Project name
- `description` - Project description
- `start_date` - Start date
- `end_date` - End date
- `status` - Status (planning, in_progress, completed, archived)
- `lead_researcher_id` - FK to users.id

### AI Agents Table
- `id` - UUID primary key
- `name` - Agent name
- `model_id` - FK to ai_models.id
- `configuration` - JSON configuration
- `owner_user_id` - FK to users.id
- `status` - Status (active, inactive, testing)

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Revert migrations
flask db downgrade
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Using Supabase Edge Functions

See deployment guide in the main project documentation.

## Security Considerations

1. **Password Hashing:** All passwords are hashed using Werkzeug security
2. **JWT Tokens:** Secure token-based authentication with expiration
3. **CORS:** Configured to allow only trusted origins
4. **SQL Injection:** Protected through SQLAlchemy ORM
5. **Data Encryption:** Sensitive data fields are encrypted
6. **HIPAA Compliance:** Audit logs and access controls

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
psql -U user -d health_tech_db

# Verify DATABASE_URL in .env
```

### JWT Token Errors

- Ensure `JWT_SECRET` is set in environment variables
- Check token expiration time
- Verify token format in Authorization header

### CORS Issues

- Add frontend URL to `CORS_ORIGINS` in .env
- Restart the server after changing CORS settings

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## License

© 2024 Health Tech Ecosystem. All rights reserved.

## Support

For issues and questions, please contact the development team or submit an issue in the repository.
