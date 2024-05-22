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


Screenshots from app
<img width="1677" alt="Screenshot 2024-05-22 at 13 27 04" src="https://github.com/berkanyuce/full_stack_data_science_project/assets/61622650/83428947-a080-47e6-8a80-b007db7da01f">
<img width="1677" alt="Screenshot 2024-05-22 at 13 27 30" src="https://github.com/berkanyuce/full_stack_data_science_project/assets/61622650/73b3e36b-b447-463f-885b-d159c0253e51">
<img width="1677" alt="Screenshot 2024-05-22 at 13 27 40" src="https://github.com/berkanyuce/full_stack_data_science_project/assets/61622650/545a050d-bc03-4555-8569-560285b6522f">
<img width="1677" alt="Screenshot 2024-05-22 at 13 27 47" src="https://github.com/berkanyuce/full_stack_data_science_project/assets/61622650/6365272c-bcc3-4107-99d5-5477667c138f">
<img width="1677" alt="Screenshot 2024-05-22 at 13 28 09" src="https://github.com/berkanyuce/full_stack_data_science_project/assets/61622650/89b59bc7-0bcb-4762-9085-1dde30e6468f">
