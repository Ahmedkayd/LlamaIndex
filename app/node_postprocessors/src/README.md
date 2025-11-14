#  LlamaIndex ChatBot Using ChromaDB & Streamlit (Dockerized)

## Requirements
This project sets up a complete document ingestion and retrieval pipeline using:

- [LlamaIndex](https://github.com/jerryjliu/llama_index)
- [ChromaDB](https://www.trychroma.com/)
- [Streamlit](https://streamlit.io/)
- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- [Docker-compose](https://docs.docker.com/compose/install/linux/)
- [openAI API-Key](https://platform.openai.com)

## 📂 Project Structure
```text
├── docker-compose.yml
├── Dockerfile
├── README.md
├── app/
│   ├── app.py                # Streamlit frontend
│   ├── ingestion.py          # Ingests documents into ChromaDB
│   ├── node_postprocessors/  # node postprocessor to optimize node processing
│   └── llamaindex-docs/      # Folder containing input .html document files
├── chroma_data/              # Persistent ChromaDB storage
├── requirements/             # pip packages to be installed
```
## To run this code locally, you’ll need to:
While this code is configured to use OpenAI, you can use any LLM. If you choose to use a different LLM, be sure to update the code as needed and configure it to connect to your chosen model.
This project is containerized and you can simply run the below commands to test it locally on your machine.

- Install `docker and docker-compose` on your machine.
- Obtain an OpenAI API key.
- clone this repo `git clone git@bitbucket.org:saccounty/dha-dau-miscellaneous-ahmed.git`
- Go to llamaindex directory in the terminal.
- Add your openAI api-key in .env file as `OPENAI_API_KEY=xyz`
- Run `docker-compose up`
- Go to [http://localhost:8504](http://localhost:8504) 

![](src/llamaindex.png)
