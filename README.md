# 🐐 Uptime Goat Node

This repository contains the `goat_report` and `endpoint_agent` scripts. The `goat_report` script periodically sends asynchronous reports to the [**Cryptards**](https://cryptards.lol/) Uptime Goat servers. The `endpoint_agent` script periodically fetches the endpoints where `goat_report` needs to send the reports to.

![Uptime Goat](assets/goattime.jpg)

## 🚀 Features

- **Asynchronous Requests**: Uses `aiohttp` to make fast, concurrent requests to multiple endpoints.
- **Goat Monitoring**: Tracks consecutive goat report numbers and logs when these reset unexpectedly.
- **Docker Ready**: A pre-built image is available for seamless deployment.

## 🐙 Quick Start with Docker Compose (recommended)

We recommend using Docker Compose to run the script as this is the most robust.

**Prerequisites**:

- Docker Compose
- Docker
- Git

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Ducktatorrr/uptime-goat-node.git
   cd uptime-goat-node/app
   ```

2. **Create a `.env` file**:

   ```bash
   cp .env.example .env
   ```

3. **Open the `.env` file and set the `GOAT_ID` and `GOAT_KEY` variables**:

   ```bash
   GOAT_ID=<token_here>
   GOAT_KEY=<key_here>
   ENDPOINTS_URL=<PREFILLED>
   ```

   Replace `<token_here>` with your actual 32-character hexadecimal GOAT_ID and GOAT_KEY.

   You should not change the `ENDPOINTS_URL` variable unless you know what you are doing.

4. **Run the Docker Compose command**:

   ```bash
   docker compose up -d
   ```

5. **Check the logs**:
   ```bash
   docker compose logs -f
   ```

### Stopping & Updating the deployment

To stop the deployment, use:

```bash
docker compose down
```

When a new version is released pull the repository and rebuild the images:

```bash
git pull
```

To update all the containers in the deployment:

```bash
docker compose pull
docker compose up -d --build
```

To update a specific service (example Endpoint Agent):

```bash
docker compose up -d --build endpoint-agent
```

This automatically rebuilds the image and restarts the service.

## 🐋 Quick Start with balena (for the Cryptards)

If you want to run this on a device like a Raspberry Pi, Orange Pi or other single board computer, you can run this app using balenaCloud for free.

Simply click the "Deploy with balena" button below (you will need to create an account if you haven't already got one):

[![Deploy with button](https://www.balena.io/deploy.svg)](https://dashboard.balena-cloud.com/deploy?repoUrl=https://github.com/Ducktatorrr/uptime-goat-node&defaultDeviceType=raspberrypi4-64)

You will then need to add a `Device Variable` with the name `GOAT_ID` and another with the name `GOAT_KEY`. The values should be set information you got from the [Onboarding - Uptime GOAT page](https://cryptards.lol/onboard). You should not change the `ENDPOINTS_URL` variable unless you know what you are doing.

## 📦 Quick Start with Docker (strongly discouraged)

To run the goat report node using Docker, follow these steps:

1. **Pull the pre-built Docker image**:

   ```bash
   docker pull ghcr.io/ducktatorrr/uptime-goat-node/combined:latest
   ```

2. **Run the container**:

   ```bash
   docker run --restart always --name uptime_goat -d -e GOAT_ID=<token_here> -e GOAT_KEY=<key_here> -e ENDPOINTS_URL=https://raw.githubusercontent.com/1rabbit/goat_servers/refs/heads/main/uptime_endpoints ghcr.io/ducktatorrr/uptime-goat-node/combined:latest
   ```

   - Replace `<token_here>` with your actual 32-character hexadecimal GOAT_ID and GOAT_KEY.

   This will start the container in detached mode (`-d`), with automatic restart enabled (`--restart always`), ensuring the container always stays up.

   To live view the logs, use:

   ```bash
   docker logs uptime_goat -f
   ```

### Stopping & Updating the container

To stop the container, use:

```bash
docker stop uptime_goat
```

To remove the container:

```bash
docker rm uptime_goat
```

To update the container:

```bash
docker pull ghcr.io/ducktatorrr/uptime-goat-node/combined:latest
```

Then you can start the container again with the same command as above.

## 🐍 Quick Start with Python

If you want to run the script locally without Docker:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Ducktatorrr/uptime-goat-node.git
   cd uptime-goat-node/app
   ```

2. **Create a virtual environment and activate it**:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Copy the `.env.example` file to `.env`**:

   ```bash
   cp .env.example .env
   ```

5. **Open the `.env` file and set the `GOAT_ID` and `GOAT_KEY` variables**:

   ```bash
   GOAT_ID=<token_here>
   GOAT_KEY=<key_here>
   ENDPOINTS_URL=<PREFILLED>
   ```

   Replace `<token_here>` with your actual 32-character hexadecimal GOAT_ID and GOAT_KEY.

   You should not change the `ENDPOINTS_URL` variable unless you know what you are doing.

6. **Run the scripts**:
   ```bash
   python goat_report.py
   python endpoint_agent.py
   ```

## 🛠 Configuration

- **GOAT_ID and GOAT_KEY**: A 32-character hexadecimal token for authenticating with the goat servers. You can pass this token and key as an environment variable (`-e GOAT_ID=<token_here> -e GOAT_KEY=<key_here>`).

- **Endpoints**: The script sends reports to the following endpoints:

  - `supgoat`: [https://supgoat.cryptards.lol/report](https://supgoat.cryptards.lol/report)
  - `hellogoat`: [https://hellogoat.cryptards.lol/report](https://hellogoat.cryptards.lol/report)
  - `iamgoat`: [https://iamgoat.cryptards.lol/report](https://iamgoat.cryptards.lol/report)

  We will keep these endpoints up to date so don't touch them.

## 🐛 Error Handling

If the request fails, the script logs the error message and retries on the next cycle. If the "consecutive" goat count resets (indicating a potential "rug pull"), the script logs this with the message `RUGGED 💀`.

## 🎉 Contributing

We welcome contributions! Feel free to submit issues, pull requests, or feature requests.
Beware that automatic Flake8 linting is enabled so make sure your code is linted before submitting a PR.

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
