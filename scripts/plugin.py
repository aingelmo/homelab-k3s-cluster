import json
import base64
import argparse
import sys

def cloudflare_tunnel_id(file_path: str = 'cloudflare-tunnel.json') -> str:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        tunnel_id = data.get("TunnelID")
        if tunnel_id is None:
            raise KeyError(f"Missing 'TunnelID' key in {file_path}")
        return tunnel_id

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Could not decode JSON file: {file_path}")
    except KeyError as e:
        raise KeyError(f"Error in JSON structure: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while processing {file_path}: {e}")

def cloudflare_tunnel_secret(file_path: str = 'cloudflare-tunnel.json') -> str:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        transformed_data = {
            "a": data["AccountTag"],
            "t": data["TunnelID"],
            "s": data["TunnelSecret"]
        }
        json_string = json.dumps(transformed_data, separators=(',', ':'))
        return base64.b64encode(json_string.encode('utf-8')).decode('utf-8')

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Could not decode JSON file: {file_path}")
    except KeyError as e:
        raise KeyError(f"Missing key in JSON file {file_path}: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while processing {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cloudflare tunnel utility.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_secret = subparsers.add_parser("secret", help="Encode Cloudflare tunnel secret JSON for Kubernetes secret usage.")
    parser_secret.add_argument("file_path", nargs="?", default="cloudflare-tunnel.json", help="Path to the Cloudflare tunnel JSON file")

    parser_id = subparsers.add_parser("id", help="Get the Cloudflare TunnelID from the JSON file.")
    parser_id.add_argument("file_path", nargs="?", default="cloudflare-tunnel.json", help="Path to the Cloudflare tunnel JSON file")

    args = parser.parse_args()
    try:
        if args.command == "secret":
            print(cloudflare_tunnel_secret(args.file_path))
        elif args.command == "id":
            print(cloudflare_tunnel_id(args.file_path))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)

