FROM python:3
SHELL [ "/bin/bash", "-c"]

RUN apt update && apt install -y sudo vim bash-completion

# Create a user dev
RUN useradd -rm -d /home/dev -s /bin/bash -g root -G sudo -u 1001 dev
# Set the default password of user dev to `dev`
# Set the default password of user `root` to `root`
RUN echo 'dev:dev' | chpasswd && echo 'root:root' | chpasswd
# Set the default user to `dev` for the following instructions
USER dev
# Set the working directory to the home of user `dev` for the following instructions
WORKDIR /home/dev

RUN git clone https://github.com/magicmonty/bash-git-prompt.git ~/.bash-git-prompt --depth=1 \
    && echo "if [ -f \"$HOME/.bash-git-prompt/gitprompt.sh\" ]; then" >> ~/.bashrc \
    && echo "    GIT_PROMPT_ONLY_IN_REPO=1" >> ~/.bashrc \
    && echo "    source $HOME/.bash-git-prompt/gitprompt.sh" >> ~/.bashrc \
    && echo "fi" >> ~/.bashrc

# Exposing "~/.local/bin" where pipenv will be installed
ENV PATH="/home/dev/.local/bin:${PATH}"
RUN pip install --user pipenv