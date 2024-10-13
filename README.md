# 🐐 Goat Report Script

This repository contains the `goat-report` script that periodically sends asynchronous reports to the **Cryptards** Uptimet Goat servers. It monitors consecutive goat report numbers and logs any "rug pulls" (i.e., when the count resets unexpectedly). The script is pre-built as a Docker image, making it easy to run in any environment.

## 🚀 Features

- **Asynchronous Requests**: Uses `aiohttp` to make fast, concurrent requests to multiple endpoints.
- **Goat Monitoring**: Tracks consecutive goat report numbers and logs when these reset unexpectedly.
- **Docker Ready**: A pre-built image is available for seamless deployment.

## 📦 Quick Start with Docker

To run the goat report script using Docker, follow these steps:

1. **Pull the pre-built Docker image**:

   ```bash
   docker pull ghcr.io/ducktatorrr/uptime-goat-node:latest
   ```

2. **Run the container**:

   ```bash
   docker run --restart always --name uptime_goat -d -e GOAT_TOKEN=<token_here> ghcr.io/ducktatorrr/uptime-goat-node:latest
   ```

   - Replace `<token_here>` with your actual 32-character hexadecimal GOAT_TOKEN.

   This will start the container in detached mode (`-d`), with automatic restart enabled (`--restart always`), ensuring the container always stays up.

   To live view the logs, use:

   ```bash
   docker logs uptime_goat -f
   ```

### Stopping & Updating the container

To stop the container, use:

```bash
docker stop goat_uptime
```

To remove the container:

```bash
docker rm goat_uptime
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

5. **Open the `.env` file and set the `GOAT_TOKEN` variable**:

   ```bash
   GOAT_TOKEN=<token_here>
   ```

   Replace `<token_here>` with your actual 32-character hexadecimal GOAT_TOKEN.

6. **Run the script**:
   ```bash
   python goat_report.py
   ```

## 🛠 Configuration

- **GOAT_TOKEN**: A 32-character hexadecimal token for authenticating with the goat servers. You can pass this token as an environment variable (`-e GOAT_TOKEN=<token_here>`).

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
