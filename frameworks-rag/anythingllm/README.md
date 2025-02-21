# Getting started
- Update the .env file as needed
- Create the folder for the volume binding. E.g.: `mkdir -p ./data/anythingllm`
- Create or put the env file of anythingllm. E.g.: `touch ./data/anythingllm/.env`
- Start the framework using `docker compose up -d`

# Post install tuning
- If the framework hasn't been started in multiuser mode, go to settings, security and toggle the multiuser switch on , ceate teh first admin user and save