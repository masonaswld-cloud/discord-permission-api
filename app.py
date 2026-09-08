from flask import Flask, jsonify
import os
import requests

app = Flask(__name__)

PERMISSIONS = {
    1: "Create Invite",
    2: "Kick Members",
    4: "Ban Members",
    8: "Administrator",
    16: "Manage Channels",
    32: "Manage Server",
    64: "Add Reactions",
    128: "View Audit Log",
    256: "Priority Speaker",
    512: "Stream",
    1024: "View Channel",
    2048: "Send Messages",
    4096: "Send TTS Messages",
    8192: "Manage Messages",
    16384: "Embed Links",
    32768: "Attach Files",
    65536: "Read Message History",
    131072: "Mention Everyone",
    262144: "Use External Emojis",
    524288: "View Server Insights",
    1048576: "Connect",
    2097152: "Speak",
    4194304: "Mute Members",
    8388608: "Deafen Members",
    16777216: "Move Members",
    33554432: "Use Voice Activity",
    67108864: "Change Nickname",
    134217728: "Manage Nicknames",
    268435456: "Manage Roles",
    536870912: "Manage Webhooks",
    1073741824: "Manage Expressions",
    2147483648: "Use Application Commands",
    4294967296: "Request to Speak",
    8589934592: "Manage Events",
}


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Discord Permission API is running"
    })


@app.route("/role/<role_id>")
def get_role_permissions(role_id):
    token = os.environ.get("DISCORD_BOT_TOKEN")
    guild_id = os.environ.get("DISCORD_GUILD_ID")

    if not token or not guild_id:
        return jsonify({
            "error": "API is not configured"
        }), 500

    url = f"https://discord.com/api/v10/guilds/{guild_id}/roles"

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bot {token}"
        }
    )

    if response.status_code != 200:
        return jsonify({
            "error": "Could not get Discord roles",
            "status": response.status_code
        }), response.status_code

    roles = response.json()

    for role in roles:
        if role["id"] == role_id:
            permission_number = int(role["permissions"])

            names = [
                name
                for value, name in PERMISSIONS.items()
                if permission_number & value
            ]

            return jsonify({
                "role_id": role["id"],
                "role_name": role["name"],
                "permissions": names
            })

    return jsonify({
        "error": "Role not found"
    }), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
