# from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The IDs and Ranges of the Google Sheets to read on startup
SPREADSHEET_ID_OG = '1IBg12lkldnF3h5W2CleGUL25w3yLdc0uPiPHuhVDr34'
SPREADSHEET_ID_DC = '1s2rE7cu9HWaFUAnVoRmri7hmo-Kj2w0ri9yq6W0ebDE'
SPREADSHEET_ID_MZ = '1_9XSjAg2vAKybPohpJkti3-3G-OPcLJmqCS1vOpMcZQ'
SPREADSHEET_RANGE_1E = '1E Survivor!A2:L'
SPREADSHEET_RANGE_2E = '2E Survivor!A2:L'
SPREADSHEET_RANGE_DC = 'Heroes!A2:T'
SPREADSHEET_RANGE_FAN = 'Fantasy!A2:L'
SPREADSHEET_RANGE_MZ = 'Heroes!A2:U'
SPREADSHEET_RANGE_NLD = 'NotLD!A2:J'
SPREADSHEET_RANGE_SCI = 'SciFi!A2:M'
SPREADSHEET_RANGE_WES = 'Western!A2:M'
SPREADSHEET_RANGE_Z1E = '1E Zombivor!A2:K'
SPREADSHEET_RANGE_Z2E = '2E Zombivor!A2:L'
SPREADSHEET_RANGE_ZDC = 'Zombies!A2:T'
SPREADSHEET_RANGE_ZMZ = 'Zombies!A2:T'

# The Tables to populate from the Google Sheets on startup
# table_1e = None
# table_2e = None
# table_dc = None
# table_fan = None
# table_mz = None
# table_nld = None
# table_sci = None
# table_wes = None
# table_z1e = None
# table_z2e = None
# table_zdc = None
# table_zmz = None


# Reads all sheets to populate tables, used on startup
def populate_tables():
    try:
        # service = build('sheets', 'v4', credentials=creds,client_options={'quota_project_id': '<your project ID>'})
        service = build('sheets', 'v4',
                        credentials=Credentials.from_authorized_user_file('token.json', SCOPES),
                        client_options={'quota_project_id': 'abotmination'}
                        )

        # Sheet: Zombicide Survivor Skill List  --  Tab: 1E Survivor
        global table_1e
        print('Loading data: 1E')
        table_1e = read_sheet(service, SPREADSHEET_ID_OG, SPREADSHEET_RANGE_1E)

        # Sheet: Zombicide Survivor Skill List  --  Tab: 2E Survivor
        global table_2e
        print('Loading data: 2E')
        table_2e = read_sheet(service, SPREADSHEET_ID_OG, SPREADSHEET_RANGE_2E)

        # Sheet: DCeased - Master List  --  Tab: Heroes
        global table_dc
        print('Loading data: DC')
        table_dc = read_sheet(service, SPREADSHEET_ID_DC, SPREADSHEET_RANGE_DC)

        # Sheet: Zombicide Survivor Skill List  --  Tab: Fantasy
        global table_fan
        print('Loading data: FAN')
        table_fan = read_sheet(service, SPREADSHEET_ID_OG, SPREADSHEET_RANGE_FAN)

        # Sheet: Marvel Zombies - Master List  --  Tab: Heroes
        global table_mz
        print('Loading data: MZ')
        table_mz = read_sheet(service, SPREADSHEET_ID_MZ, SPREADSHEET_RANGE_MZ)

        # Sheet: Zombicide Survivor Skill List  --  Tab: NotLD
        global table_nld
        print('Loading data: NLD')
        table_nld = read_sheet(service, SPREADSHEET_ID_OG, SPREADSHEET_RANGE_NLD)

        # Sheet: Zombicide Survivor Skill List  --  Tab: SciFi
        global table_sci
        print('Loading data: SCI')
        table_sci = read_sheet(service, SPREADSHEET_ID_OG, SPREADSHEET_RANGE_SCI)

        # Sheet: Zombicide Survivor Skill List  --  Tab: Western
        global table_wes
        print('Loading data: WES')
        table_wes = read_sheet(service, SPREADSHEET_ID_OG, SPREADSHEET_RANGE_WES)

        # Sheet: Zombicide Survivor Skill List  --  Tab: 1E Zombivor
        global table_z1e
        print('Loading data: Z1E')
        table_z1e = read_sheet(service, SPREADSHEET_ID_OG, SPREADSHEET_RANGE_Z1E)

        # Sheet: Zombicide Survivor Skill List  --  Tab: 2E Zombivor
        global table_z2e
        print('Loading data: Z2E')
        table_z2e = read_sheet(service, SPREADSHEET_ID_OG, SPREADSHEET_RANGE_Z2E)

        # Sheet: DCeased - Master List  --  Tab: Zombies
        global table_zdc
        print('Loading data: ZDC')
        table_zdc = read_sheet(service, SPREADSHEET_ID_DC, SPREADSHEET_RANGE_ZDC)

        # Sheet: Marvel Zombies - Master List  --  Tab: Zombies
        global table_zmz
        print('Loading data: ZMZ')
        table_zmz = read_sheet(service, SPREADSHEET_ID_MZ, SPREADSHEET_RANGE_ZMZ)

    except HttpError as err:
        print(err)

# Read a single sheet and return its data, helper method to populate_tables()
def read_sheet(service, id, range):
    sheet = service.spreadsheets()
    data = (
        sheet.values()
        .get(spreadsheetId=id, range=range)
        .execute()
    )
    values = data.get('values', [])

    if not values:
        print('No data found.\n')
    else:
        print('Data loaded.\n')
    
    return values

# Find a row in the specified table with the specified value in column A
async def find_row(table, value):
    for row in table:
        if row[0].lower() == value.lower():
            return row
    return None

# Sheet: Zombicide Survivor Skill List  --  Tab: 1E Survivor
async def search_1e(prompt):
    data = await find_row(table_1e, prompt)
    if not data:
        return

    title = data[0]
    description = await survivor_skills(data, 3, 3)

    return title, description

# Sheet: Zombicide Survivor Skill List  --  Tab: 1E Survivor
async def search_2e(prompt):
    data = await find_row(table_2e, prompt)
    if not data:
        return
    
    title = data[0]
    description = ''
    if data[3] != '---': # Used in the sheet to mean 'no data' in optional fields
        description += 'Special: ' + data[3] + '\n\n'
    description += await survivor_skills(data, 4, 2)

    return title, description

# Sheet: DCeased - Master List  --  Tab: Heroes
async def search_dc(prompt):
    data = await find_row(table_dc, prompt)
    if not data:
        return
    
    # handles spawn card being missing
    spawn = ['N/a', 'No spawn card found.']
    if len(data) > 17 and data[17] != '' and data[16] != '':
        spawn[0] = data[17]
        spawn[1] = data[16]
    title = data[0]
    description = (
        ':purple_square: **' + data[4] + '**\n'
        + data[5] + ': ' + data[6] + '/' + data[7] + '/' + data[8]
        + '\n\n:blue_square: **' + data[9] + '**\n' + str.replace(data[10], '*', '\*')
        + '\n\n:yellow_square: **' + data[11] + '**\n' +
        + '\n\n:orange_square: **' + data[12] + '**\n' + str.replace(data[13], '*', '\*')
        + '\n\n:red_square: **' + data[14] + '**\n' + str.replace(data[15], '*', '\*')
        + '\n\n\n\n:brown_square: **SPAWN CARD ABILITY**\nToughness: '
        + spawn[0] + '\n' + spawn[1]
    )
    return title, description

# Sheet: Zombicide Survivor Skill List  --  Tab: Fantasy
async def search_fan(prompt):
    data = await find_row(table_fan, prompt)
    if not data:
        return

    title = data[0]
    description = ''
    if data[3] != '---': # Used in the sheet to mean 'no data' in optional fields
        description += 'Item Slot: ' + data[3] + '\n\n'
    description += await survivor_skills(data, 4, 2)

    return title, description

# Sheet: Marvel Zombies - Master List  --  Tab: Heroes
async def search_mz(prompt):
    data = await find_row(table_mz, prompt)
    if not data:
        return

    # handles spawn card being missing
    spawn = ['N/a', 'No spawn card found.']
    if len(data) > 19 and data[19] != '' and data[18] != '':
        spawn[0] = data[19]
        spawn[1] = data[18]
    title = data[0]
    description = (
        ':purple_square: **' + data[5] + '**\n'
        + data[6] + ': ' + data[7] + '/' + data[8] + '/' + data[9]
        + '\n\n:blue_square: **' + data[10] + '**\n' + str.replace(data[11], '*', '\*')
        + '\n\n:yellow_square: **' + data[12] + '**\n' + str.replace(data[13], '*', '\*')
        + '\n\n:orange_square: **' + data[14] + '**\n' + str.replace(data[15], '*', '\*')
        + '\n\n:red_square: **' + data[16] + '**\n' + str.replace(data[17], '*', '\*')
        + '\n\n\n\n:brown_square: **SPAWN CARD ABILITY**\nToughness: '
        + spawn[0] + '\n' + spawn[1]
    )
    return title, description

# Sheet: Zombicide Survivor Skill List  --  Tab: NotLD
async def search_nld(prompt):
    data = await find_row(table_nld, prompt)
    if not data:
        return

    title = data[0]
    description = ''
    if data[2] != '---': # Used in the sheet to mean 'no data' in optional fields
        description += 'Mode: ' + data[2] + '\n\n'
    description += await survivor_skills(data, 3, 1)

    return title, description

# Sheet: Zombicide Survivor Skill List  --  Tab: SciFi
async def search_sci(prompt):
    data = await find_row(table_sci, prompt)
    if not data:
        return

    title = data[0]
    description = ''
    if data[3] != '---': # Used in the sheet to mean 'no data' in optional fields
        description += 'Class: ' + data[3] + '\n'
    if data[4] != '---':
        description += 'Squad: ' + data[4] + '\n\n'
    description += await survivor_skills(data, 5, 2)

    return title, description

# Sheet: Zombicide Survivor Skill List  --  Tab: Western
async def search_wes(prompt):
    data = await find_row(table_wes, prompt)
    if not data:
        return

    title = data[0]
    description = ''
    if data[3] != '---': # Used in the sheet to mean 'no data' in optional fields
        description += 'Class: ' + data[3] + '\n'
    if data[4] != '---':
        description += 'Item Slot: ' + data[4] + '\n\n'
    description += await survivor_skills(data, 5, 2)

    return title, description

# Sheet: Zombicide Survivor Skill List  --  Tab: 1E Zombivor
async def search_z1e(prompt):
    data = await find_row(table_z1e, prompt)
    if not data:
        return

    title = data[0]
    description = await survivor_skills(data, 3, 2)

    return title, description

# Sheet: Zombicide Survivor Skill List  --  Tab: 2E Zombivor
async def search_z2e(prompt):
    data = await find_row(table_z2e, prompt)
    if not data:
        return

    title = data[0]
    description = await survivor_skills(data, 4, 2)

    return title, description

# Sheet: DCeased - Master List  --  Tab: Zombies
async def search_zdc(prompt):
    data = await find_row(table_zdc, prompt)
    if not data:
        return

    # handles spawn card being missing
    spawn = ['N/a', 'No spawn card found.']
    if len(data) > 18 and data[18] != '' and data[17] != '':
        spawn[0] = data[17]
        spawn[1] = data[16]

    title = data[0]
    description = (
        '\n\n\n\n:brown_square: **SPAWN CARD ABILITY**\nToughness: '
        + spawn[0] + '\n' + spawn[1]
    )
    return title, description

# Sheet: Marvel Zombies - Master List  --  Tab: Zombies
async def search_zmz(prompt):
    data = await find_row(table_zmz, prompt)
    if not data:
        return

    # handles spawn card being missing
    spawn = ['N/a', 'No spawn card found.']
    if len(data) > 18 and data[18] != '' and data[17] != '':
        spawn[0] = data[18]
        spawn[1] = data[17]

    title = data[0]
    description = (
        ':purple_square: **' + data[4] + '**\n'
        + data[5] + ': ' + data[6] + '/' + data[7] + '/' + data[8]
        + '\n\n:blue_square: **' + data[9] + '**\n' + str.replace(data[10], '*', '\*')
        + '\n\n:yellow_square: **' + data[11] + '**\n' + str.replace(data[12], '*', '\*')
        + '\n\n:orange_square: **' + data[13] + '**\n' + str.replace(data[14], '*', '\*')
        + '\n\n:red_square: **' + data[15] + '**\n' + str.replace(data[16], '*', '\*')
        + '\n\n\n\n:brown_square: **SPAWN CARD ABILITY**\nToughness: '
        + spawn[0] + '\n' + spawn[1]
    )
    return title, description

async def survivor_skills(data=[], index=0, num_blue=1):
    skills = ''
    for x in range(0, num_blue):
        if data[index] != '' and data[index] != '---':
            skills += ':blue_square: ' + data[index] + '\n'
        index += 1

    skills += '\n:yellow_square: ' + \
        data[index] + '\n\n:orange_square: ' + data[index + 1]
    index += 2

    if data[index] != '' and data[index] != '---':
        skills += '\n:orange_square: ' + data[index]
    skills += '\n\n:red_square: ' + data[index + 1]
    index += 2

    if data[index] != '' and data[index] != '---':
        skills += '\n:red_square: ' + \
            data[index] + '\n:red_square: ' + data[index + 1]

    return skills
