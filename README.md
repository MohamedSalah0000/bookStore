# Online Book Store
##### Description: Platform is a virtual bookstore where users can read and review books.

## Instalitation & usage 

- Clone the repository
- Build and run the Docker containers: `docker compose up --build`
- Swagger API docs `http://localhost:8000/api/docs`
- Django admin `http://localhost:8000/admin`
- Create superuser `docker compose -f compose.yml run --rm django python manage.py createsuperuser`
- Run tests `docker compose -f compose.yml run django python manage.py test apps`
