# AmazoniaHack-Ibama-Fiscalizators

Using Flask, PSQL and JavaScript, the project give a interface to upload and process images took during Ibama's operations and visualize them on a interactive map.

** Group ** : Alexandria Baraza, Guilherme Felitti, Marcela Jimenez, Sermírian Amôedo and Sihan Zhang

Map from [Sihan Zhang's repository](https://github.com/SihanZhang98/amazonia-hack)

[Our video presenting how the webapp works](https://www.loom.com/share/2c41e8cc70e74576bd9ebd387437505a?sid=7d7ee550-aadd-49a5-ae6d-b08c4a346190)

### Challenge Statement
The challenge is to develop an automated solution that creates a comprehensive georeferenced database and map system for timestamped data in Brazil. This system must seamlessly integrate with the existing item stamp app used by two distinct user groups - Guards and IBAMA's management teams. The primary objective is to enable users to easily upload, visualize, and analyze both historical and new timestamped data on a map of Brazil, while also efficiently tracking the user types responsible for capturing photos and videos. The solution should be inherently flexible to accommodate future expansion and integration with additional data sources, such as Planet images and mapbiomas data. 

Currently, IBAMA inspectors use the TimeStamp app to register their visits to the field, however this app does not allow an automatic viewing of the areas' data history and the data geolocation map. For this project, you will have access to this sample to use as part of your solution development.

*Suggested Goals*:
- Create a fully functioning prototype of a geolocated map
- Develop comprehensive wireframes for the app, offering a clear visual blueprint for its design and functionality
- Implement basic upload/download functionality within the app


## Prerequisites

Before you begin, ensure you have the following tools installed on your machine:
[Git](https://git-scm.com), [pyenv](https://github.com/pyenv/pyenv), [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) (optional but recommended).

## Installation

Follow these steps to set up your development environment and run the project locally.

### Cloning the Repository

Clone the repository to your local machine using `git`:

```
git clone https://github.com/gfelitti/AmazoniaHack-Ibama-Fiscalizators.git
cd AmazoniaHack-Ibama-Fiscalizators
```

### Setting Up pyenv and Creating a Virtual Environment

If not already installed, install the desired Python version using pyenv:


```
pyenv install 3.9.1  # Replace with your preferred Python version
```

### Create a virtual environment for the project (if using pyenv-virtualenv):

```
pyenv virtualenv 3.9.1 your_project-env
```

### Activate the virtual environment:

```
pyenv activate your_project-env
```

### Installing Dependencies

Install the project dependencies using pip:

```
pip install -r requirements.txt
```

### Configuring Environment Variables

Rename the .envexample file to .env at the project root and insert your environment variables, such as API keys, database connection strings, etc.

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@db_address:port/db_name
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
S3_BUCKET=your_bucket_name
PROMPT_VISION=prompt_to_use_with_LLM
```

### Running the Application

With everything set up, you can start the Flask server locally:

```
flask run
```
The application will be available at http://localhost:5000.


## TO DO
- Deploy the webapp on the cloud (not just the S3 bucket and the RDS)
- Connect the map with the photos API
