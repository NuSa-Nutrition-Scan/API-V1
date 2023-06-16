# Install This Project Locally

This guide will walk you through the steps required to install and run this project locally on your machine.

## Prerequisites

Before getting started, make sure you have the following prerequisites installed:

- Python 3.10.5 or higher
- pip 23.1.2 or higher
- Machine learning instance that run somewhere

## Steps

1. **Setup Google Cloud Storage bucket**

   Create a Google Cloud Storage bucket to store the project's data. Make note of the bucket name and ensure you have the necessary access credentials.

2. **Setup Firebase**

   Create a Firebase project and set it up for use with this project. You will need the Firebase project credentials and configuration details.

3. **Enable Firebase Authentication and Firestore**

   Enable Firebase Authentication and Firestore services in your Firebase project. These services are required for user authentication and data storage.

4. **Generate service account both for Google Cloud Storage and Firebase**

   Generate a service account key for Google Cloud Storage and Firebase. This will provide the necessary credentials for accessing the respective services.

5. **Generate Web API Key in Firebase**

   Generate a Web API Key in the Firebase project console. This key will be used for authentication and API access.

6. **Clone this project**

   Clone this project repository to your local machine using Git.

7. **Install the requirements**

   Navigate to the project directory and install the required Python dependencies by running the following command:

    ```
    pip install -r requirements.txt
    ```
    This will install all the dependencies you need.

8. **Copy the .env.example to .env**

   In the project directory, make a copy of the `.env.example` file and rename it to `.env`. This file will contain environment-specific configuration settings.

    ```
    cp .env.example .env
    ```

9. **Fill the environment variables**

   Open the `.env` file in a text editor and fill in the necessary environment variables based on your setup. Provide the required credentials and configuration details for Google Cloud Storage, Firebase, and other services.

10. **Run uvicorn**

     Start the project's server using the following command:
     ```
     uvicorn main:app --reload
     ```
     This will run the project using the Uvicorn ASGI server and enable live reloading for development.

Congratulations! You have successfully installed this project locally. You can now access the project through your web browser or API client using the provided URLs and endpoints.

## Troubleshooting

If you encounter any issues during the installation process, please contact us.


