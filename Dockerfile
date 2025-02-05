FROM python:3-slim-buster

# Upgrade pip
RUN pip install --upgrade pip

# Environment variables
ENV USER botx
ENV HOME /home/$USER
ENV BOT $HOME/media-search-bot

# Add user and setup working directory
RUN useradd -m $USER
RUN mkdir -p $BOT
WORKDIR $BOT

# Change ownership and switch to the created user
RUN chown $USER:$USER $BOT
USER $USER

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose the Flask port
EXPOSE 8000

# Start the bot and Flask
CMD ["sh", "-c", "python3 bot.py"]
