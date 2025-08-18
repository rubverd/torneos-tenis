from app import create_app
import os
app = create_app()
    # Railway necesita escuchar en 0.0.0.0 y puerto que viene de $PORT
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
