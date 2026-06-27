# Implementation Plan - Performance Profiling with Django Silk

This plan details the installation and secure configuration of Django Silk for performance monitoring. Access will be restricted strictly to superusers, with convenient navigation links added to the Django Admin panel and the sidebar menu.

## User Review Required

> [!IMPORTANT]
> - **Dependency Installation**: We will install `django-silk` in the project's virtual environment.
> - **Database Migrations**: Django Silk uses database tables to store profiling data. We will run `python manage.py migrate` after configuration.
> - **Superuser-Only Access**: Access to the `/silk/` route will be restricted to superusers via the `SILKY_PERMISSIONS` setting.

## Proposed Changes

### Configuration and Dependencies

#### [MODIFY] [settings.py](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda_project/settings.py)
- Add `'silk'` to `INSTALLED_APPS`.
- Add `'silk.middleware.SilkyMiddleware'` to `MIDDLEWARE`.
- Set `'DIRS': [BASE_DIR / 'templates']` in `TEMPLATES` to allow overriding Django Admin templates.
- Define Silk configurations at the bottom:
  ```python
  SILKY_AUTHENTICATION = True
  SILKY_AUTHORISATION = True
  SILKY_PERMISSIONS = lambda user: user.is_superuser
  ```

#### [MODIFY] [urls.py](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda_project/urls.py)
- Include `'silk.urls'` at the path `silk/`.

### Frontend & Navigation

#### [NEW] [base_site.html](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/templates/admin/base_site.html)
- Create a custom admin template that extends `admin/base.html` and overrides the `nav-global` block to display a "Ver Rendimiento (Silk)" button (styled cleanly) linking to `/silk/`.

#### [MODIFY] [base.html](file:///c:/Users/I5/Documents/CODIGO/AGENDA_PAOLA/agenda/templates/agenda/base.html)
- Add a conditional submenu item `"Rendimiento (Silk)"` under the "Profesor" menu section, visible only if `user.is_superuser` is `True`.

## Verification Plan

### Automated Tests
- Run `venv\Scripts\python.exe manage.py check` to verify imports and configurations.
- Run `venv\Scripts\python.exe manage.py migrate` to apply Silk migrations.

### Manual Verification
- Log in as a superuser, navigate to the Django Admin home page, and verify the "Ver Rendimiento (Silk)" link is visible and functional.
- In the sidebar menu, expand the "Profesor" dropdown and verify "Rendimiento (Silk)" appears.
- Log in as a regular professor (non-superuser) or student and verify that the links are NOT visible and that navigating directly to `/silk/` yields a permission/authorization error.
