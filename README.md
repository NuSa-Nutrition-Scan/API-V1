# NuSa API v1

NuSa API v1 provides the backend API for our application, enabling seamless communication between the client-side application and the server. This API is designed to power our nutrition tracking and analysis platform, allowing users to manage their nutrition data and interact with various features.

### Team: 
Cloud Computing

## Features

### Authentication section
- **Register:** Register an user.
- **Login**: Authenticate users and generate access tokens.
- **Logout**: Invalidate access tokens and log out users.
- **Refresh**: Refresh expired access tokens.

### Settings section
- **Update profile**: Allow users to update their profile information.
- **See history**: Provide access to a user's activity history.

### Nutrition
- **Personal food recommendation**: Get the users' food recommendations based on their data
- **Upload food photo**: Enable users to upload photos of their meals or food items.
- **Scan food photo**: Scan photo of the food to get the result of it.
- **Set max upload**: Limit the number of photo scans to 10 per day.

## Tech Stack

- **Python + FastAPI**: The API is built using Python with the FastAPI framework, which offers high performance and easy-to-use tools for building web APIs.
- **Google Cloud Storage**: Used for storing uploaded photos securely and efficiently.
- **Google App Engine**: Provides a scalable platform for deploying and managing the API in the cloud.
- **Firebase Authentication**: Handles user authentication, ensuring secure access to the API.
- **Firestore**: A NoSQL document database provided by Firebase, used for storing and retrieving user data and activity history.

## Getting Started

To set up the project locally and start developing or testing the API, please follow the steps outlined in our [Installation Guide](https://github.com/NuSa-Nutrition-Scan/API-V1/blob/main/INSTALL.md).

If you want to start consuming the API immediately, please refer to our [API Documentation](https://nusa-api-dot-nusa-nutrition-scan-387706.as.r.appspot.com/docs).

## License

This project is licensed under the [MIT License](https://github.com/NuSa-Nutrition-Scan/API-V1/blob/main/LICENSE).
