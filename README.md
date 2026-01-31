# Voice AI SaaS

A Django-based SaaS platform for managing voice AI campaigns and call automation.

## Features

- **Multi-tenancy**: Isolated data and configurations per tenant
- **User Management**: JWT-based authentication with role-based access
- **Voice Campaigns**: Create and manage automated voice campaigns
- **Call Management**: Track and manage voice calls with real-time status
- **Provider Integration**: Extensible voice provider system (mock implementation included)
- **Analytics**: Comprehensive call analytics and reporting
- **Async Processing**: Celery-based background task processing

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Async Tasks**: Celery with Redis
- **API Documentation**: DRF built-in browsable API

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd voice_ai_saas
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   - Create a PostgreSQL database named 'voice_ai_saas'
   - Update database credentials in `backend/backend/settings.py`

5. **Run migrations**
   ```bash
   cd backend
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

1. **Start Django development server**
   ```bash
   python manage.py runserver
   ```

2. **Start Celery worker** (in a separate terminal)
   ```bash
   celery -A backend worker --loglevel=info
   ```

3. **Start Redis server** (if not already running)
   ```bash
   redis-server
   ```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login

### Campaigns
- `GET /api/campaigns/` - List campaigns
- `POST /api/campaigns/` - Create campaign
- `GET /api/campaigns/{id}/` - Get campaign details
- `PUT /api/campaigns/{id}/` - Update campaign
- `DELETE /api/campaigns/{id}/` - Delete campaign
- `POST /api/campaigns/{id}/activate/` - Activate campaign
- `POST /api/campaigns/{id}/pause/` - Pause campaign
- `POST /api/campaigns/{id}/complete/` - Complete campaign

### Calls
- `GET /api/calls/` - List calls
- `POST /api/calls/` - Create call
- `GET /api/calls/{id}/` - Get call details
- `PUT /api/calls/{id}/` - Update call
- `DELETE /api/calls/{id}/` - Delete call
- `POST /api/calls/{id}/initiate/` - Initiate call
- `POST /api/calls/{id}/hangup/` - Hang up call
- `GET /api/calls/stats/` - Get call statistics

### Analytics
- `GET /api/analytics/overview/` - Get analytics overview
- `GET /api/analytics/campaigns/` - Get campaign analytics
- `GET /api/analytics/calls/` - Get call analytics

## Project Structure

```
voice_ai_saas/
├── backend/
│   ├── manage.py
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── accounts/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── tenants/
│   │   ├── models.py
│   │   ├── middleware.py
│   │   └── admin.py
│   ├── campaigns/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── voice_providers/
│   │   ├── base.py
│   │   ├── mock_provider.py
│   │   └── services.py
│   ├── calls/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tasks.py
│   └── analytics/
│       └── views.py
├── requirements.txt
└── README.md
```

## Development

### Adding New Voice Providers

1. Create a new provider class inheriting from `VoiceProvider`
2. Implement all abstract methods
3. Add the provider to `VoiceProviderService.providers`
4. Update settings and database configurations as needed

### Testing

```bash
cd backend
python manage.py test
```

### Code Formatting

```bash
black .
isort .
```

## Deployment

1. Set `DEBUG = False` in settings.py
2. Configure production database settings
3. Set up proper static file serving
4. Configure Celery with production broker
5. Use gunicorn or uwsgi for serving Django

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
