from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# The IDs and Ranges of the Google Sheets to read on startup
SPREADSHEET_ID_OG = '1IBg12lkldnF3h5W2CleGUL25w3yLdc0uPiPHuhVDr34'
SPREADSHEET_ID_DC = '1s2rE7cu9HWaFUAnVoRmri7hmo-Kj2w0ri9yq6W0ebDE'
SPREADSHEET_ID_MZ = '1_9XSjAg2vAKybPohpJkti3-3G-OPcLJmqCS1vOpMcZQ'
SPREADSHEET_RANGE_1E = '1E Survivor!A2:N'
SPREADSHEET_RANGE_2E = '2E Survivor!A2:N'
SPREADSHEET_RANGE_DC = 'Heroes!A:U'
SPREADSHEET_RANGE_FAN = 'Fantasy!A2:N'
SPREADSHEET_RANGE_MZ = 'Heroes!A:U'
SPREADSHEET_RANGE_NLD = 'NotLD!A2:N'
SPREADSHEET_RANGE_SCI = 'SciFi!A2:N'
SPREADSHEET_RANGE_WES = 'Western!A2:N'
SPREADSHEET_RANGE_Z1E = '1E Zombivor!A2:N'
SPREADSHEET_RANGE_Z2E = '2E Zombivor!A2:N'
SPREADSHEET_RANGE_ZDC = 'Zombies!A:U'
SPREADSHEET_RANGE_ZMZ = 'Zombies!A:U'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
sheet_reader = build('sheets', 'v4',
                credentials=Credentials.from_authorized_user_file('token.json', SCOPES),
                client_options={'quota_project_id': 'abotmination'}
                )

def populate_sheets():
    try:
        # Sheet: Zombicide Survivor Skill List  --  Tab: 1E Survivor
        global sheet_1e
        print('Loading data: 1E...', end='')
        sheet_1e = Sheet(SPREADSHEET_ID_OG, SPREADSHEET_RANGE_1E)

        # Sheet: Zombicide Survivor Skill List  --  Tab: 2E Survivor
        global sheet_2e
        print('Loading data: 2E...', end='')
        sheet_2e = Sheet(SPREADSHEET_ID_OG, SPREADSHEET_RANGE_2E, 'Special')

        # Sheet: DCeased - Master List  --  Tab: Heroes
        global sheet_dc
        print('Loading data: DC...', end='')
        sheet_dc = HeroSheet(SPREADSHEET_ID_DC, SPREADSHEET_RANGE_DC)

        # Sheet: Zombicide Survivor Skill List  --  Tab: Fantasy
        global sheet_fan
        print('Loading data: FAN...', end='')
        sheet_fan = Sheet(SPREADSHEET_ID_OG, SPREADSHEET_RANGE_FAN, 'Item Slot')

        # Sheet: Marvel Zombies - Master List  --  Tab: Heroes
        global sheet_mz
        print('Loading data: MZ...', end='')
        sheet_mz = HeroSheet(SPREADSHEET_ID_MZ, SPREADSHEET_RANGE_MZ)

        # Sheet: Zombicide Survivor Skill List  --  Tab: NotLD
        global sheet_nld
        print('Loading data: NLD...', end='')
        sheet_nld = Sheet(SPREADSHEET_ID_OG, SPREADSHEET_RANGE_NLD, 'Mode')

        # Sheet: Zombicide Survivor Skill List  --  Tab: SciFi
        global sheet_sci
        print('Loading data: SCI...', end='')
        sheet_sci = Sheet(SPREADSHEET_ID_OG, SPREADSHEET_RANGE_SCI, 'Class', 'Squad')

        # Sheet: Zombicide Survivor Skill List  --  Tab: Western
        global sheet_wes
        print('Loading data: WES...', end='')
        sheet_wes = Sheet(SPREADSHEET_ID_OG, SPREADSHEET_RANGE_WES, 'Class', 'Item Slot')

        # Sheet: Zombicide Survivor Skill List  --  Tab: 1E Zombivor
        global sheet_z1e
        print('Loading data: Z1E...', end='')
        sheet_z1e = Sheet(SPREADSHEET_ID_OG, SPREADSHEET_RANGE_Z1E, 'Special')

        # Sheet: Zombicide Survivor Skill List  --  Tab: 2E Zombivor
        global sheet_z2e
        print('Loading data: Z2E...', end='')
        sheet_z2e = Sheet(SPREADSHEET_ID_OG, SPREADSHEET_RANGE_Z2E, 'Special')

        # Sheet: DCeased - Master List  --  Tab: Zombies
        global sheet_zdc
        print('Loading data: ZDC...', end='')
        sheet_zdc = HeroSheet(SPREADSHEET_ID_DC, SPREADSHEET_RANGE_ZDC)

        # Sheet: Marvel Zombies - Master List  --  Tab: Zombies
        global sheet_zmz
        print('Loading data: ZMZ...', end='')
        sheet_zmz = HeroSheet(SPREADSHEET_ID_MZ, SPREADSHEET_RANGE_ZMZ)

    except HttpError as err:
        print(err)

class Sheet:
    def __init__(self, sheet_id, sheet_range, trait_1 = None, trait_2 = None):
        data = (
            sheet_reader.spreadsheets().values()
            .get(spreadsheetId=sheet_id, range=sheet_range)
            .execute()
        ).get('values', [])
        
        if not data:
            print('No data found.')
        else:
            print('Data loaded.')
        
        self.data = data
        self.trait_1 = trait_1
        self.trait_2 = trait_2

    # Returns the raw data of the row found with 'value' in the first column
    async def find_row(self, value):
        for row in self.data:
            if row[0].lower() == value.lower():
                return row
        return
    
    # Same as find_row() but does some basic formatting for settings where it applies
    async def search(self, value):
        row = await self.find_row(value)
        if not row:
            return
        
        title = row[0]
        description = 'Set: ' + row[1] + '\n'
        if self.trait_1 and row[3] != '---' and row[3] != '':
            description +=  self.trait_1 + ': ' + row[3] + '\n'
        if self.trait_2 and row[4] != '---' and row[4] != '':
            description += self.trait_2 + ': ' + row[4] + '\n'
        description += '\n'

        for i in range(5,8):
            if row[i] != '---' and row[i] != '':
                description += ':blue_square: ' + row[i] + '\n'
        description += '\n:yellow_square: ' + row[8] + '\n\n'
        for i in range(9,11):
            if row[i] != '---' and row[i] != '':
                description += ':orange_square: ' + row[i] + '\n'
        description += '\n'
        for i in range(11,14):
            if row[i] != '---' and row[i] != '':
                description += ':red_square: ' + row[i] + '\n'

        return title, description
    
class HeroSheet(Sheet):
    def __init__(self, sheet_id, sheet_range):
        super().__init__(sheet_id, sheet_range)
        self.health_col = self.data[0][4].lower() == 'health'
        self.yellow_desc = self.data[0][12 + self.health_col].lower() == 'yellow skill description'

    async def search(self, value):
        row = await self.find_row(value)
        if not row:
            return
        
        title = row[0]
        description = 'Set: ' + row[1] + '\n\n'
        index = 4 + self.health_col
        if row[index] != '':
            description += (
                ':purple_square: **' + row[index] + '**\n' + row[index + 1] + ': ' + row[index + 2]  
                + '/' + row[index + 3] + '/' + row[index + 4]
                + '\n\n:blue_square: **' + row[index + 5] + '**\n' + str.replace(row[index + 6], '*', '\*')
                + '\n\n:yellow_square: **' + row[index + 7] + '**' 
            )
            if self.yellow_desc == 1 and row[index+8] != '':
                description += '\n' + str.replace(row[index + 8], '*', '\*')
            index += 8 + self.yellow_desc
            description += (
                '\n\n:orange_square: **' + row[index] + '**\n' + str.replace(row[index + 1], '*', '\*')
                + '\n\n:red_square: **' + row[index + 2] + '**\n' + str.replace(row[index + 3], '*', '\*')
                + '\n\n\n'
            )

        spawn = ['N/a', 'No Spawn Card Found']
        index = 16 + self.health_col + self.yellow_desc
        if len(row) > index + 1:
            spawn[0] = row[index + 1] if row[index + 1] != '' else 'N/a'
            spawn[1] = row[index] if row[index] != '' else 'No Spawn Card Found'
        description += (
            ':brown_square: **SPAWN CARD ABILITY**\nToughness: '
            + spawn[0] + '\n' + spawn[1]
        )
        return title, description