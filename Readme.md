# API de Google 

Para la creacion del API de Google seguir los siguientes pasos con **python3 y docker!**

## Instalar Python y Create venv para desarrollo

- instalar python 3
- pip install virtualenv
- cd compliance-duediligence-google
- python3 -m venv .\venvapi\
- .\venvapi\Scripts\activate.ps1

## instalar paquetes en el venv

- pip install Flask
- pip install numpy

## Activar Virtual Env

- cd compliance-duediligence-google
- .\venvapi\Scripts\activate.ps1

## Instalar del requirements.txt (activar en venv)

- pip install -r requirements.txt

## Generar el requirements.txt

- pipdeptree (mirar las dependencias)
- pip3 freeze > requirements.txt

## Ejecutar Flask

- flask run

## Sequence Diagram Due Diligence Google

```mermaid
sequenceDiagram
Compliance Flow->> Compliance Google API: Verify apellido, nombre y ID if had bad news
Compliance Google API-->>Cosmos: get setup search metadata for google
Note right of Cosmos: Read GoogleSetupContainer
Compliance Google API-->>Compliance Google API: prepare query for google (wish, veto y otros)
Note right of Compliance Google API: Create querys using conditionals<br/> to call google api
loop Compliance Check for wish, veto y otros
	Compliance Google API-->>Google API: execute query
	Compliance Google API-->>Cosmos:store results 
	Note right of Cosmos: Write GoogleTrack
end
Compliance Google API-->>Cosmos:query information stored 
Note right of Cosmos: Read GoogleTrack for all sites stored on the previous steps
Compliance Google API-->>Compliance Google API: verify if had bad news
Compliance Google API-->>Compliance Flow: Responder si tiene Noticias negativas o no
```

## Sequence Diagram Cumplimiento

```mermaid
sequenceDiagram
FrontEnd->> Compliance Flow: send apellido, nombre y ID
Compliance Flow-->> Compliance Google API: Verify apellido, nombre y ID bad news
Compliance Flow-->> Compliance Inteligo API: Verify Workcheck and PEP
Compliance Flow-->> Compliance Flow: Consolidate information checked
Compliance Flow-->> FrontEnd: Has bad news and is on black list
```