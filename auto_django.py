import os
import subprocess

def create_django_project(project_name):
    # Step 1: Start a new Django project
    subprocess.run(['django-admin', 'startproject', project_name])

    # Step 2: Start a new app in the project called 'index'
    os.chdir(project_name)
    subprocess.run(['python', 'manage.py', 'startapp', 'index'])

    # Step 3: Add 'index' to the installed app list in settings.py
    with open(os.path.join(project_name, 'settings.py'), 'r+') as settings_file:
        settings_content = settings_file.read()
        settings_content = settings_content.replace(
            "INSTALLED_APPS = [",
            "INSTALLED_APPS = [\n    'index',"
        )
        settings_file.seek(0)
        settings_file.write(settings_content)
        settings_file.truncate()

    # Step 4: Import the 'include' method in urls.py
    with open(os.path.join(project_name, 'urls.py'), 'r+') as urls_file:
        urls_content = urls_file.read()
        urls_content = urls_content.replace(
            "from django.urls import path",
            "from django.urls import path, include\n"
        )
        urls_file.seek(0)
        urls_file.write(urls_content)
        urls_file.truncate()

    # Step 5: Add the path to index.urls to the urlpatterns list in urls.py
    with open(os.path.join(project_name, 'urls.py'), 'r+') as urls_file:
        urls_content = urls_file.read()
        if "path('', include('index.urls'))" not in urls_content:
            urls_content = urls_content.replace(
                "urlpatterns = [",
                "urlpatterns = [\n    path('', include('index.urls')),"
            )
            urls_file.seek(0)
            urls_file.write(urls_content)
            urls_file.truncate()

    # Step 6: Change directory to the 'index' app folder
    os.chdir('index')

    # Step 7: Add a new urls.py file for the created index app
    with open('urls.py', 'w') as index_urls_file:
        index_urls_file.write("""from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]""")

    # Step 8: Create a new folder called “templates” in the index app
    os.makedirs('templates')

    # Step 9: Create a new html file called index.html in the templates folder
    with open(os.path.join('templates', 'index.html'), 'w') as index_html_file:
        index_html_file.write("<html><body><h1>Welcome to the index page</h1></body></html>")

    # Step 10: In views.py in the index app, add a new function called index that renders out the index.html
    with open('views.py', 'a') as views_file:
        views_file.write("def index(request):\n")
        views_file.write("    return render(request, 'index.html')\n")

    # Step 11: Move back to the main project directory
    os.chdir('../')

if __name__ == "__main__":
    project_name = input("Enter your Django project name: ")
    create_django_project(project_name)
    print(f"Django project '{project_name}' created successfully!")
