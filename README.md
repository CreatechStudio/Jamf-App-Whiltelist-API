# Jamf Mobile Configuration App Whitelist API

This API script is designed to add a bundle id to a specific configuration profile in Jamf Pro. Avoiding the need to manually add bundle ids to the whitelist in the *slooooooooow* Jamf Pro Web.

## Requirements

1. Jamf Pro Instance
2. API roles with following permission
   - Read iOS Configuration Profiles
   - Update iOS Configuration Profiles
3. API client with permission metioned in requirement 2
4. A configuration profile with at least a bundle id in whitelist.
   - Restrictions - Apps - App usage - Only some apps allowed
   - Add a bundle id to the whitelist
   - Save

## Usage

0. Clone this repository
1. (Optional) Get bundle id by using a [Rasycast Script](https://raycast.com) in [my another repositroy](https://github.com/CreatechStudio/Raycast-Script/blob/main/get-bundle-id.py)
2. Fill `JSS_URL`, `CLIENT_ID`, `CLIENT_TOKEN`, `CONFIG_ID` *(which can be found in URL)* in `update.py`
3. Prepare a bundle id you would like to add to the whitelist
4. Run `python3 update.py`

## Debug

There is a file called `parse.py` which can automaticaaly convert temp file in `jamf_api_temp` folder to a readable XML file, don't forget to change the file name which needs to be parsed in `parse.py`.

## Note

This script is designed for Jamf Pro 11.6.1, it may not work for other versions. Please test it in your test environment before using it in production.

If you want to modify this script such as enable you add a list of bundle ID etc., please feel free to raise a PR.