<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/KOSASIH/GFMS-Core">GFMS</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://www.linkedin.com/in/kosasih-81b46b5a">KOSASIH</a> is licensed under <a href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Creative Commons Attribution 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""></a></p>

# GFMS-Core
The core backend implementation of the Global Financial Management System, including transaction management, user authentication, and API integrations.

# Global Financial Management System (GFMS)

## Overview

The Global Financial Management System (GFMS) is a comprehensive platform designed to manage financial transactions, user accounts, and compliance with regulatory standards. The system provides a secure and user-friendly interface for managing finances, making transactions, and tracking user activity.

## Features

- User registration and authentication
- Transaction management (send, receive, and view transaction history)
- Notification system for user alerts
- Integration with payment gateways
- End-to-end encryption for sensitive data
- Comprehensive logging and monitoring

## Technologies Used

- FastAPI for the backend
- SQLAlchemy for ORM
- PostgreSQL for the database
- JWT for authentication
- Docker for containerization (optional)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL installed and running
- pip for package management

### Installation

1. Clone the repository:
   ```bash
   1 git clone https://github.com/KOSASIH/gfms.git
   2 cd gfms
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   1 python -m venv venv
   2 source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   
3. Install the required packages:

   ```bash
   1 pip install -r requirements.txt
   ```
   
3. Set up the environment variables:

- Create a .env file in the root directory and configure the necessary environment variables.

4. Run database migrations:

   ```bash
   1 alembic upgrade head
   ```
   
5. Start the application:

   ```bash
   1 uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   
## Running Tests
To run the automated tests, use:

   ```bash
   1 pytest tests/
   ```

## Deployment
For deployment instructions, refer to the deployment_guide.md file.

## Contributing
Contributions are welcome! Please follow the guidelines in the developer_guide.md file for contributing to the project.

## License
This project is licensed under the MIT License.
