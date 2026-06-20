# Walkthrough - Performance Profiling with Django Silk

Django Silk has been integrated and configured with the following details:

1. **Installation & Configuration**:
   - Installed `django-silk` and `gprof2dot` in the virtual environment.
   - Configured [settings.py](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda_project/settings.py):
     - Added `'silk'` to `INSTALLED_APPS` and `'silk.middleware.SilkyMiddleware'` to `MIDDLEWARE`.
     - Enabled `'templates'` root folder in `TEMPLATES['DIRS']`.
     - Configured superuser-only access:
       ```python
       SILKY_AUTHENTICATION = True
       SILKY_AUTHORISATION = True
       SILKY_PERMISSIONS = lambda user: user.is_superuser
       ```
   - Added path routing in [urls.py](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda_project/urls.py) directing `/silk/` to `silk.urls`.
   - Run migrations to create Silk's database tables successfully.

2. **Navigation Links**:
   - **Django Admin Panel**: Overrode [base_site.html](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/templates/admin/base_site.html) to display a **⚡ Ver Rendimiento (Silk)** button at the top header for superusers.
   - **Professor Menu Sidebar**: Modified [base.html](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda/templates/agenda/base.html) to append a **Rendimiento (Silk)** link under the "Profesor" section, guarded by a `user.is_superuser` check so it is completely hidden from students and regular professors.
