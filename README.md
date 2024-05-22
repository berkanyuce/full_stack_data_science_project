After clone repo, open the directory on your terminal.
For backend:
  1) This promp will create database
    conda activate # If you use an conda env.
    python3
    import models
    import services
    services.create_database()

  2) This runs your server
     uvicorn main:app --reload

For frontend:
  npm install
  npm start
