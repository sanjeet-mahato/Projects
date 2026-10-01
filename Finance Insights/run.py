import uvicorn
from app.services.apploadconfig import config


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=config["server"]["host"],
        port=config["server"]["port"],
        reload=config["server"]["reload"],
    )
