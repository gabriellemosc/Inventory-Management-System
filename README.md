<h1 align="center"> SmartStock </h1>


![descrição da imagem](https://github.com/gabriellemosc/Inventory-Management-System/blob/main/Screen_Photos/Screenshot%20from%202025-09-22%2009-36-56.png)



## ✔️ Techniques and technologies used

- ``Python 3.12.3``
- ``JavaScript``
- ``Django``
- ``HTML``
- ``CSS``
- ``SQLite``
- ``OOP``

  ## 🚀 About

***Inventory Management*** System is a Django-based project designed to efficiently manage and organize product inventory. Created for learning and practice purposes, it implements essential features of an inventory system, such as product registration, quantity control, categories, CRUD operations, and stock movements. The project focuses on modularity and flexibility, allowing for future expansions and easy testing.

- Product Organization: Enables structuring products into categories and managing essential information, simulating a real inventory management system.
- User Management: Supports different access levels with Admin and User modes, ensuring control over sensitive operations and system security.
- Filtering and Searching: Allows filtering products by price, category, quantity, or other relevant information, facilitating navigation and decision-making.
- Stock Movements & Reports: Tracks product inflows and outflows, with the option to download detailed reports on inventory and stock movements.
- Scalability: The modular design allows easy integration of additional features, such as low-stock alerts or new types of reports.
- Maintainability: The code is organized to support easy maintenance and adaptation, making it simple to implement new features and improvements.

## 🛠️ Getting Started
1. **Clone the repository**  
  - Clone the repository to your local machine:

   ```bash
    git clone https://github.com/gabriellemosc/Inventory-Management-System.git
    cd Inventory-Management-System
   ```
2. **Create and Activate the Virtual Environment**  
- To keep dependencies organized, create a Python virtual environment and activate it:
    ```bash

    # Linux / macOS
  python3 -m venv venv
  source venv/bin/activate
  
  # Windows (PowerShell)
  python -m venv venv
  venv\Scripts\activate

  ```

3. Install Dependencies
- After activating the virtual environment, install the required Python packages:
```bash
pip install -r requirements.txt
```

4. **Config the DataBase and SuperUser**  
- a) Modify the Database Settings in settings.py
    Modify the `settings.py` file to adjust the database settings for your environment.
    By default, Django uses SQLite, but you can switch to PostgreSQL or MySQL if preferred.

    Example for SQLite (default):
  
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
      ```
- b) ***Create the Database and Migrations***
      After configuring the database, create the necessary tables with the following commands:
  
  ```bash
  
      python manage.py makemigrations
      python manage.py migrate

  ```

  
- c) **Create a Django Superuser**
    To access the Django admin panel, you will need a superuser:
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

Here are some screenshots of the **SmartStock** project, showing the main features and user interface.

| Movement Stock Report | Minimum Stock Alert | Category List |
| --- | --- | --- |
| ![Movement Stock Report](https://github.com/gabriellemosc/Inventory-Management-System/blob/main/Screen_Photos/Screenshot%20from%202025-09-22%2010-37-28.png) | ![Movie Details Page](https://github.com/gabriellemosc/Inventory-Management-System/blob/main/Screen_Photos/Screenshot%20from%202025-09-22%2010-36-02.png) | ![Category_List](https://github.com/gabriellemosc/Inventory-Management-System/blob/main/Screen_Photos/Screenshot%20from%202025-09-22%2010-40-09.png) |



## License

This project is licensed under the MIT License. See the file [LICENSE](./LICENSE) for more details.


- ## Author

<h3> <a href="https://github.com/gabriellemosc">Gabriel L. </a></h3>


Description: Backend Developer


