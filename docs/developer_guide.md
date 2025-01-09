# Developer Guide

## Introduction

This guide is intended for developers who want to contribute to the Global Financial Management System (GFMS).

## Setting Up the Development Environment

1. **Clone the Repository**: 
   ```bash
   1 git clone https://github.com/KOSASIH/gfms.git
   2 cd gfms
   ```

2. **Install Dependencies**:

   ```bash
   1 pip install -r requirements.txt
   ```
   
3. Set Up Environment Variables: Create a .env file and configure the necessary environment variables.

### Code Structure
- src/: Contains the main application code.
- docs/: Contains documentation files.
- tests/: Contains unit and integration tests.

### Running the Application
To run the application locally, use:

   ```bash
   1 uvicorn src.main:app```bash
   2 --reload
   ```

### Testing
To run the tests, use:

   ```bash
   1 pytest tests/
   ```

## Contributing

1. Fork the Repository: Create your own fork of the repository.
2. Create a Branch:
   ```bash
   1 git checkout -b feature/your-feature-name
   ```
   
3. Make Changes: Implement your feature or fix.
4. Commit Your Changes:
   ```bash
   1 git commit -m "Add your message here"
   ```
   
5. Push to Your Branch:
   ```bash
   1 git push origin feature/your-feature-name
   ```
   
6. Create a Pull Request: Submit a pull request to the main repository for review.

## Best Practices
- Follow the coding standards and style guidelines.
- Write unit tests for new features.
- Document your code and changes appropriately.
