# 🐐 Goat Report Script

This repository contains the `goat-report` script that periodically sends asynchronous reports to the [**Cryptards**](https://cryptards.lol/) Uptime Goat servers. It monitors consecutive goat report numbers and logs any "rug pulls" (i.e., when the count resets unexpectedly). The script is pre-built as a Docker image, making it easy to run in any environment.

![Uptime Goat](assets/goattime.jpg)

## 🚀 Features

- **Asynchronous Requests**: Uses `aiohttp` to make fast, concurrent requests to multiple endpoints.
- **Goat Monitoring**: Tracks consecutive goat report numbers and logs when these reset unexpectedly.
- **Docker Ready**: A pre-built image is available for seamless deployment.

## 🐙 Quicks tart with Docker Compose (recommended)

We recommend using Docker Compose to run the script as this is the most robust.

**Prerequisites**:

- Docker Compose
- Docker
- Git

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Ducktatorrr/uptime-goat-node.git
   cd app
   ```

2. **Create a `.env` file**:

   ```bash
   cp .env.example .env
   ```

3. **Open the `.env` file and set the `GOAT_ID` and `GOAT_KEY` variables**:

   ```bash
   GOAT_ID=<token_here>
   GOAT_KEY=<key_here>
   ```

   Replace `<token_here>` with your actual 32-character hexadecimal GOAT_ID and GOAT_KEY.

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

## 📦 Quick Start with Docker

To run the goat report script using Docker, follow these steps:

1. **Pull the pre-built Docker image**:

   ```bash
   docker pull ghcr.io/ducktatorrr/uptime-goat-node:latest
   ```

2. **Run the container**:

   ```bash
   docker run --restart always --name uptime_goat -d -e GOAT_ID=<token_here> -e GOAT_KEY=<key_here> ghcr.io/ducktatorrr/uptime-goat-node:latest
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
docker pull ghcr.io/ducktatorrr/uptime-goat-node:latest
```

Then you can start the container again with the same command as above.

## 🐍 Quick Start with Python

If you want to run the script locally without Docker:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/goat-report.git
   cd goat-report
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
   ```

   Replace `<token_here>` with your actual 32-character hexadecimal GOAT_ID and GOAT_KEY.

6. **Run the script**:
   ```bash
   python goat_report.py
   ```

## 🛠 Configuration

- **GOAT_ID and GOAT_KEY**: A 32-character hexadecimal token for authenticating with the goat servers. You can pass this token and key as an environment variable (`-e GOAT_ID=<token_here> -e GOAT_KEY=<key_here>`).

- **Endpoints**: The script sends reports to the following endpoints:

  - `supgoat`: [https://supgoat.cryptards.lol/report](https://supgoat.cryptards.lol/report)
  - `hellogoat`: [https://hellogoat.cryptards.lol/report](https://hellogoat.cryptards.lol/report)

  We will keep these endpoints up to date so don't touch them.

## 🐛 Error Handling

If the request fails, the script logs the error message and retries on the next cycle. If the "consecutive" goat count resets (indicating a potential "rug pull"), the script logs this with the message `RUGGED 💀`.

## 🎉 Contributing

We welcome contributions! Feel free to submit issues, pull requests, or feature requests.

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
