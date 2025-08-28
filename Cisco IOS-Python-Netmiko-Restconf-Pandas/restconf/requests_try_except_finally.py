import requests
requests.packages.urllib3.disable_warnings()

TEST_URI = "https://10.254.0.1:443/restconf/"
dash = "-" * 80

def main():
    print(dash)
    try:
        r = requests.get(TEST_URI, auth=("cisco", "cisco"), verify=False)
        r.raise_for_status()
    except requests.ConnectionError as e:
        output = e
    except requests.HTTPError as e:
        output = e
    else:
        output = r.content
    finally:
        print(output)
        print(dash)

if __name__ == "__main__":
    main()
