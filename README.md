# Enhancing Interactivity and Cognition in 3D Scenes Using Large Language Models
 
## Directory Overview

This project consists of several component. Most notably the Unity project, the annoation tool and services that take an assisting role. As well as our automated labeling solution.

![Example image](images/system_architecture.png)

| Subdirectory | Description                 |
|--------------|-----------------------------|
| [annotation-tool](./Subdir1/README.md) | User interface to annotate models add documents, upload models |
| Subdir2      | [README](./Subdir2/README.md) |
| Subdir3      | [README](./Subdir3/README.md) |


## How to run

To simplify running all services except the Unity project we utilize docker-compose 

```
git clone https://git.tu-berlin.de/furkantas/bachelor-source-code.git
cd TODO
docker-compose up -d
```



## asset search
it is important to note that the database provided here only contains 30,000 elements instead of the ...





### chat-server
POST to localhost:5000 to ask ChatGPT. </br>
ChatGPT knows actions and responds with a action

### chromadb-cap3d
Cap3D is labels for Objaverse and ABO Dataset. </br>
Loaded Cap3D into ChromaDB for search. </br>
Download glb from Objaverse from search.

### object-relationship
ThreeJS example of object relationship

### threejs
one 3d asset and chatgpt







# NOTES

- asset search
- authoring tool
- image api
- rag
- labeling


# TODO
- gucken ob threejs functioniert in other (es initial threejs)
- API Keys entfernen
- automated labeling machen was du versprichst
- docker und docker-compose
- Text hier durch ChatGPT jagen
- individuelle readme
- mit anderem projekt mergen
