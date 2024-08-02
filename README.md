<div align="center">
  <h1>Apache Airflow + Astro</h1>
  <p>This repository leverages Astronomer's <a href="https://www.astronomer.io/docs/astro/cli/overview">Astro CLI</a>, a powerful tool for running Apache Airflow.</p> 
</div>

**Table of Contents**

  - [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Working with Docker](#working-with-docker)
  - [Debugging](#debugging)
  - [Navigating the Project](#navigating-the-project)

**Why Astro?**

<sup><sub>I know this might sound like an ad for Astronomer, but hear me out—this is all coming from personal experience. :D</sub></sup>

> As someone who's worked on automating the deployment of Airflow, both <a href="https://github.com/julie-scherer/airflow-local">locally</a> and <a href="https://github.com/julie-scherer/airflow-docker">in Docker</a>, I know firsthand how arduous and complicated the setup requirements can be, even for local environments. The <a href="https://www.astronomer.io/docs/astro/runtime-image-architecture">Astro Runtime Docker image</a> streamlines Airflow and Docker integration by abstracting complexities, simplifying Airflow project management. This is huge when you think about setting up, configuring, and maintaining an Airflow project at a company with multiple deployment environments, along with the need to set up underlying cloud infrastructure and CI/CD pipelines.
> 
> I can just see the human labor costs adding up...
> 
> Astro simplifies the setup process by providing a consistent environment across both local and production instances and offering robust <a href="https://www.astronomer.io/docs/astro/automation-overview">CI/CD support</a> that streamlines the development and deployment cycle. Additionally, Astro offers comprehensive monitoring and logging capabilities, making it easier to debug and optimize workflows over time. I also love the simple commands for development and deployment that the Astro CLI provides (I'm someone who's always adding a Makefile to my projects so I can do everything in one command, lol).
> 
> As a personal anecdote, one of my top favorite things about Astro is its documentation. IMO, Airflow's documentation can be challenging to navigate and extract meaningful information from, but Astro's documentation is clear, thorough, and incredibly helpful. Whether I'm trying to understand a bit of code, debugging, or staying up to date with the latest features offered by Airflow and Astro, I always turn to the <a href="https://www.astronomer.io/docs/">Astronomer Docs</a>.
> 
> Disclaimer: I’m a die-hard Mac user, and it’s clear that the Astro CLI was designed with Mac users in mind (lol). I once worked at a company where everyone else used PCs and they'd been using Astro for a while. While this isn't a dealbreaker, I have to admit that I’ve never encountered the same installation or debugging issues as my unfortunate PC user friends.


<hr>

# Getting Started 🚀

### Prerequisites

1. **Install [Docker](https://docs.docker.com/engine/install/)**: Docker is a platform for packaging, distributing, and managing applications in containers.
2. **Install the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli)**: Astro CLI is a command-line tool designed for working with Apache Airflow projects, streamlining project creation, deployment, and management for smoother development and deployment workflows.

### Local Development

1. **Clone the Repository**: Open a terminal, navigate to your desired directory, and clone the repository.
    - If you don’t have SSH configured with the GitHub CLI, please follow the instructions for [generating a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and [adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?tool=cli) in the GitHub docs.
2. **Docker Setup and Management**: Launch Docker Daemon or open the Docker Desktop app
3. **Run the Astro Project**:
    - Start Airflow on your local machine by running **`astro dev start`**
        - This will spin up 4 Docker containers on your machine, each for a different Airflow component:
            - **Postgres**: Airflow's Metadata Database, storing internal state and configurations.
            - **Webserver**: Renders the Airflow UI.
            - **Scheduler**: Monitors, triggers, and orchestrates task execution for proper sequencing and resource allocation.
            - **Triggerer**: Triggers deferred tasks.
        - Verify container creation with **`docker ps`**
    - **Access the Airflow UI**: Go to http://localhost:8081/ and log in with '**`admin`**' for both Username and Password
        >
        > ℹ️ Note: Running astro dev start exposes the Airflow Webserver at port **`8081`** and Postgres at port **`5431`**.
        >
        > If these ports are in use, halt existing Docker containers or modify port configurations in **`.astro/config.yaml`**.
        > 
4. **Stop** the Astro Docker container by running **`astro dev stop`**
    >
    > ❗🚫❗  Remember to stop the Astro project after working to prevent issues with Astro and Docker ❗🚫❗
    >
    

**⭐️ TL;DR - Astro CLI Cheatsheet ⭐️** 

```bash
astro dev start # Start airflow
astro dev stop # Stop airflow
astro dev restart # Restart the running Docker container
astro dev kill # Remove all astro docker components
```

## Working with Docker

> :bulb: **Understanding Docker Images and Containers** :whale:
> 
> Docker provides isolated environments for running applications across different systems. Docker images provide the blueprint for encapsulating an application's code, libraries, and dependencies into a portable unit, while containers represent running instances of those images.
> 
> In simple terms, Docker creates "boxes" for specific software. These boxes contain all the instructions and tools the software needs to run. Docker also takes pictures of these boxes and all their contents, called images, to use later. When you want to use the software, you tell Docker to build one of these images, and that creates a real working "box" called a container.
> 
> To learn more, explore Docker's official [Getting Started](https://docs.docker.com/get-started/) guide. I also highly recommend watching this [YouTube video](https://www.youtube.com/watch?v=pg19Z8LL06w) by TechWorld with Nana.
> 

**Here are some helpful commands to remember as you get used to working with Docker:**

- To check if you have any running Docker containers, use:
    ```bash
    docker ps      # List all available containers
    docker container ls   # Equivalent to above
    docker ps -a     # List running containers
    docker container ls -a   # Equivalent to above
    ```
    
- To list all Docker images locally:
    ```bash
    docker images
    ```
    
- Use the command below to remove an image. This is useful to free up space when you have unused images. Replace `<IMAGE ID>` with the actual image ID, which you can find by running **`docker images`**.
    ```bash
    docker rmi <IMAGE ID>
    ```
    
- Use the **`docker prune`** command to remove/reset Docker resources. This is especially handy to clean up resources and reclaim disk space.
    ```bash
    docker images prune
    docker container prune
    docker volume prune
    docker system prune
    ```
    
- To learn more about Docker, check out these resources below:
    - [Docker Overview](https://docs.docker.com/get-started/)
    - Enhance your Docker knowledge with this enlightening [YouTube Tutorial](https://www.youtube.com/watch?v=pg19Z8LL06w) by TechWorld with Nana


## Debugging

If the Airflow UI isn't updating, the project seems slow, Docker behaves unexpectedly, or other issues arise, first remove Astro containers and rebuild the project:

- Run these commands:
    ```bash
    # Stop all locally running Airflow containers
    astro dev stop
    
    # Kill all locally running Airflow containers
    astro dev kill
    
    # Remove Docker container, image, and volumes
    docker ps -a | grep astro-airflow-pipeline | awk '{print $1}' | xargs -I {} docker rm {}
    docker images | grep ^astro-airflow-pipeline | awk '{print $1}' | xargs -I {} docker rmi {}
    docker volume ls | grep astro-airflow-pipeline | awk '{print $2}' | xargs -I {} docker volume rm {}
    
    # In extreme cases, clear everything in Docker
    docker system prune
    ```
    
- Restart Docker Desktop.
- (Re)build the container image without cache.
    ```bash
    astro dev start --no-cache
    ```

## Navigating the Project

Each [Astro project](https://docs.astronomer.io/astro/develop-project) contains various directories and files. Here's an overview of how this repo is structured:

- **`dags`**: This directory houses Directed Acyclic Graphs (DAGs), which represent the workflows in Apache Airflow. Note: it's highly encouraged that you create DAGs in subfolders so that you can make use of the `.airflowignore` file when testing locally. Learn more below:
  - **`<project>/`**: Stores DAGs related to a specific project.
  - **`.airflowignore`**: Use this file to exclude folders from the Airflow scheduler, handy for local testing and avoiding production changes.
- **`Dockerfile`**: This file is based on the Astro Docker image and can be customized to include project-specific commands and/or overrides for runtime behavior. Understanding this file is optional but you're welcome to explore if you wish to dive deeper into Astro.
- **`include`** contains additional project files:
  - **`data-quality/`**...
    - **`soda/`**: Checks and configuration files for Soda checks.
  - **`datasets/`**...
    - **`videos/`**: Checks and configuration files for Soda checks.
  - **`dynamic-dags/`**...
    - **`config/`**: YAML configuration files for generating dynamic DAGs.
    - **`generators/`**: Python scripts serving as DAG generator.
    - **`templates/`**: Jinja2 templates for generating multiple identical DAGs, which are customized using the config YAML files in **`config/`**.
  - **`reusable-components/`**...
    - **`functions/`**, **`hooks/`**, **`operators/`**: Store reusable components for DAGs.
  - **`sql/`**...
    - **`<project>/*.sql`**: Stores template SQL files for DAGs. The folder name corresponds to a specific project in the DAGs folder.
- **`requirements.txt`**: Install Python packages needed for your project by adding them to this file.
- **`airflow_settings.yaml`**: Use this local-only file to define Airflow Connections, Variables, and Pools. This allows you to manage these configurations locally instead of via the Airflow UI during DAG development.


License
----------
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
