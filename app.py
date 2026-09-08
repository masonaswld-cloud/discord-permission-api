from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)
@app.route("/role")
def get_role_permissions():
    token = os.environ.get("MTUxMTQ3ODQzNzE1NDUyNTE4NA.GBIET4.35149WBj1swTtK7NN5490FaMrVtcon9GLGydb0")
    guild_id = os.environ.get("1492690243906703511")
    role_id = request.args.get("role_id")

    if not token or not guild_id or not role_id:
        return jsonify({"error": "Missing role_id"}), 400

    url = f"https://discord.com/api/v10/guilds/{guild_id}/roles/{role_id}"

    response = requests.get(
        url,
        headers={"Authorization": f"Bot {token}"}
    )

    if response.status_code != 200:
        return jsonify({
            "error": "Discord could not find this role",
            "discord_status": response.status_code,
            "role_id_received": role_id
        }), response.status_code

    role = response.json()
    permission_number = int(role["permissions"])

    names = [
        name for value, name in PERMISSIONS.items()
        if permission_number & value
    ]

    return jsonify({
        "role_id": role["id"],
        "role_name": role["name"],
        "permissions": names
    })
