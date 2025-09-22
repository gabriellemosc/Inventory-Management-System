<h1 align="center"> SmartStock </h1>


![descrição da imagem](https://github.com/gabriellemosc/Netflix_Project/blob/main/Capturas%20de%20tela/Captura%20de%20tela%20de%202024-09-23%2009-46-30.png)



## ✔️ Techniques and technologies used

- ``Python 3``
- ``Django``
- ``HTML``
- ``SQLite``
- ``OOP``

  ## 🚀 About

***Fake Netflix*** is a Django-based project designed to simulate the core features of a streaming platform. Created for learning and practice purposes, it implements key elements of a streaming service, such as movie organization, categories, and user management. The project is built with a focus on modularity and flexibility, allowing for easy future expansions and testing.
- **Content Organization**: Enables structuring of movies into categories and genres, simulating the browsing experience of a streaming catalog.- 
- **Scalability**: The modular design allows for easy integration of additional features, such as ratings and personalized movie lists.
- **Maintainability**: The code is structured to support easy maintenance and adaptation, facilitating new features and improvements.

## 🛠️ Getting Started
1. **Clone the repository**  
  - Clone the repository to your local machine:

   ```bash
   git clone https://github.com/gabriellemosc/Netflix_Project.git
   ```
2. **Create and Activate the Virtual Environment**  
- To keep dependencies organized, create a Python virtual environment and activate it:
    ```bash
  python3 -m venv venv
  source venv/bin/activate  # No Windows, use 'venv\Scripts\activate'
  ```
3. **Configuração do Banco de Dados**  
- a) Modify the Database Settings in settings.py
Open the settings.py file and change the database settings for your own environment. By default, Django uses SQLite, but you can switch to another database, such as PostgreSQL or MySQL, if you prefer.:
  Exemplo para SQLite (sem alterações):
  ```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
  }
  ```
- b) Create the Database and Migrations
    After configuring the database, create the necessary tables with the following commands:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4. **Create a Django Superuser**
- To access the Django admin panel, you will need a superuser:
    ```bash
      python manage.py createsuperuser
      ```
Follow the instructions to set the username, email and password.

5. **Start the Local Server**
- Now run the development server to see the project running:
    ```bash
      python manage.py runserver
    ```
    


## 📸 Project Screenshots

Here are some screenshots of the **Fake Netflix** project, showing the main features and user interface.

| Homepage | Movie Details Page | LoginPage |
| --- | --- | --- |
| ![Homepage](https://github.com/gabriellemosc/Netflix_Project/blob/main/Capturas%20de%20tela/Captura%20de%20tela%20de%202024-09-23%2009-46-02.png) | ![Movie Details Page](https://github.com/gabriellemosc/Netflix_Project/blob/main/Capturas%20de%20tela/Captura%20de%20tela%20de%202024-09-23%2009-46-11.png) | ![LoginPage](https://github.com/gabriellemosc/Netflix_Project/blob/main/Capturas%20de%20tela/Captura%20de%20tela%20de%202024-09-23%2009-48-21.png) |



## License

This project is licensed under the MIT License. See the file [LICENSE](./LICENSE) for more details.


- ## Author

<h3> <a href="https://github.com/gabriellemosc">Gabriel L. </a></h3>


Description: Backend Developer


