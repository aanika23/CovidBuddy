import discord
import csv
import os
from dotenv import load_dotenv
from discord.ext import commands
import process_CSV as stats

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
client = discord.Client()
bot = commands.Bot(command_prefix="!")
province = "empty"
helpType = "empty"



client = discord.Client()
botToken = "ODM4MDgwMzU4NDI3Nzg3Mjg1.YI15KA.weo9Hl9BAbdNo6r9mMcFA05CFt4"
@client.event
async def on_ready():
    print("we have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")
    
    if message.content.startswith("$stop"):
        await client.close()

    if message.content.startswith("$cv"): await Comp_Vacc(message)
    if message.content.startswith("$se"): await SideEffects(message)

    if message.content.startswith("$contact"): await contact_info(message)

    if message.content.startswith("$ts"): await Test_Site(message)

    if msg.startswith("$stats"):
        country_name = msg.split("$stats ", 1)[1]
        result = stats.get_general_stats(country_name)
        await message.channel.send(result)

    if msg.startswith("$vacInCountry"):
        country_name = msg.split("$vacInCountry ", 1)[1]
        result = stats.get_vaccines_of_country(country_name)
        await message.channel.send(result)

    if msg.startswith("$help"):
        result = ("The following are the commands I can help you with\n"
                    "\t'$cv'\t-- To compare available vaccines\n" + 
                    "\t'$contact'\t-- For COVID or Mental Health helplines\n" + 
                    "\t'$stats \"Country Name\"'\t-- For COVID statistics of a specific country\n" + 
                    "\t'$vacInCountry \"Country Name\"'\t-- For COVID vacines available in a specific country\n" + 
                    "\t'$se'\t-- For side effects of the various vaccines\n" + 
                    "\t'$ts'\t-- For COVID testing locations and their details\n")
        await message.channel.send(result)

    


@client.event
async def Comp_Vacc(message):
    if message.content == '$cv': 
        await message.channel.send("Enter any of the following to compare available vaccines:\n\n" + 
             "\t'$cv efficiency'\t-- To compare the efficiency vs. safety of the current available vaccines\n" + 
             "\t'$cv efficiency age'\t-- To compare the efficiency vs. safety of the current available vaccines by age group\n" + 
             "\t'$cv efficiency sex'\t-- To compare the efficacy of the current available vaccines by age and sex group\n" + 
             "\t'$cv side effects'\t-- To compare the side effects of the current available vaccines\n" + 
             "\t'$cv side effects age'\t-- To compare the side effects of the current available vaccines by age group\n")
    if message.content =='$cv efficiency':
        await message.channel.send(file=discord.File('vacc_img.png'))
    if message.content =='$cv efficiency age':
        await message.channel.send(file=discord.File('vacc_img_age.png'))
    if message.content =='$cv efficiency sex':
        await message.channel.send(file=discord.File('vacc_img_effective.png'))
    if message.content =='$cv side effects':
        await message.channel.send(file=discord.File('vacc_img_side.png'))
    if message.content =='$cv side effects age':
        await message.channel.send(file=discord.File('vacc_img_side_age.png'))


@client.event
async def Test_Site(message):
    if message.content == '$ts':
        await message.channel.send("Enter any of the following:\n\n" + 
            "\t'$ts \"Country Name\"'\t-- To list the testing sites in the country\n" + 
            "\t'$ts \"Country Name\" \"Province/State\"'\t-- To list the testing sites in the province/state. If there is no province/state, enter \"--\"\n" + 
            "\t'$ts \"Country Name\" \"City Name\" \"Location Name\"'\t-- To get information on the specific location\n")
    else:

        ##Open CSV File
        inputfile = open('Mock_Test_Vacc.csv')
        csv_f=csv.reader(inputfile)

        ##Get info from user input
        Mes=message.content
        MesLen=len(Mes)
        secondspace=Mes.find(' ',4)
        thirdspace=Mes.find(' ',secondspace+1)
        fourthspace=Mes.find(' ',thirdspace+1)
        fifthspace=Mes.find(' ',fourthspace+1)
        if secondspace==-1:
            countryname=Mes[4:MesLen+1]
        else:
            countryname=Mes[4:secondspace+1]

        if thirdspace==-1:
            Provname = Mes[secondspace+1:MesLen]
        else:
            Provname = Mes[secondspace+1:secondspace+3]


        cityname=Mes[thirdspace+1:MesLen+1]


        data=[]
        for row in csv_f:
            data.append(row)
        colC=[x[0] for x in data]
        colP=[x[1] for x in data]
        colCi=[x[2] for x in data]
        if secondspace==-1:
            if countryname in colC:
                for x in range(0,len(data)):
                    if countryname==data[x][0]:
                        await message.channel.send("**\n Location Name: **"+data[x][3]+"**\nProvince/State: **"+data[x][1]+"**\n City: **"+data[x][2])
                        await message.channel.send("\n______________________________________________________________________\n")
        elif thirdspace==-1:
            if Provname in colP:
                for x in range(1,len(data)):
                    if Provname==data[x][1]:
                        await message.channel.send("**\n Location Name: **"+data[x][3]+"**\nProvince/State: **"+data[x][1]+"**\n City: **"+data[x][2])
                        await message.channel.send("\n______________________________________________________________________\n")
            else:
                print("/"+Provname+"/")
        elif fourthspace==-1 or fifthspace==-1:
            if cityname in colCi:
                for x in range(2,len(data)):
                    if Provname==data[x][1]:
                        await message.channel.send("**\n Location Name: **"+data[x][3]+"**\nAddress: **"+data[x][4]+"**\nProvince/State: **"+data[x][1]+"**\n City: **"+data[x][2]+"**\nPostal Code: **"+data[x][5]+"**\nPhone Number: **"+data[x][6]+"**\nOperating Hours: **"+data[x][7]+"**\nWalk In Allowed: **"+data[x][8]+"**\nAppointment Based: **"+data[x][9]+"**\nVaccine Provided: **"+data[x][11]+"**\nMajority Vaccination type: **"+data[x][10])
                        await message.channel.send("\n______________________________________________________________________\n")
        else:
            await message.channel.send("**No Data Available at Requested Location or Wrong Format**")

        inputfile.close


@client.event
async def contact_info(message):
    if message.content == '$contact':
        await message.channel.send("Plese enter the type of help you need and your 2 letter province abbrieciation in the form of: $contact <type>-<province>\n")
    else:
        await message.channel.send("You can call " + (get_number(message)) + " for help")


def isProvince(province):
    provinces = ["BC", "AB", "SK", "MB", "ON", "QC", "NB", "NS", "PE", "NL", "NU", "NT", "TY"]
    for item in provinces:
        if province == item:
            return True
    return False

def isHelpType(helpType):
    if helpType == "covid":
        return True
    elif helpType == "mental":
        return True
    else:
        return False

def get_number(message):
    # print(message)
    info = seperateInput(message)
    if not(isHelpType(info[0]) and isProvince(info[1])):
        return "I'm sorry " + str(message.author) + " the data you asked for is not available"
    # print(info)
    rows = []
    with open("contact.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)

    # print(rows)
    i = 0
    for row in rows:
        # print(str(row[0]), str(info[1]))
        if row[0] == info[1]:
            # print(str(row[1]), str(info[0]))
            if row[1] == info[0]:
                # print("correct matching")
                return str(row[2])
        i+=1


def seperateInput(message):
    message = str(message.content)
    j = 0
    while((message[j] != " ") and (j < len(message))):
        j+=1
    message = message[j+1: len(message)]
    # print(message)

    i = 0

    while((message[i] != "-") and (i < len(message))):
        i += 1
    helpType = message[0: i]
    # print(helpType)
    province = message[i+1: i+3]
    # print(province)
    ls = []
    ls.append(helpType)
    ls.append(province)
    return ls



# get the province of user
# ask for the type of help needed (covid or mental health)
# map the resources


@client.event
async def SideEffects(message):
    if message.content=='$se':
         await message.channel.send("Enter the following to check the side effects: \n\n" + 
         "\t'$se general'\t-- General side effects of any COVID-19 Vaccine\n" + 
         "\t'$se Pfizer'\t-- Side effects of the Pfizer Vaccine\n" + 
         "\t'$se Moderna'\t-- Side effects of the Moderna Vaccine\n" + 
         "\t'$se Janssen'\t-- Side effects of the Janssen Vaccine\n" + 
         "\t'$se AstraZeneca'\t-- Side effects of the AstraZeneca Vaccine\n")
    if message.content=='$se general':
        await message.channel.send("--May include pain, redness, swelling and itchiness where the vaccine was given.\n--Some people experience local injection site reactions within 1-2 days after the vaccine, and other people experience local injection site reactions starting a week or more after they get the vaccine. \n--Local injection site reactions are a normal part of your body’s immune response to the vaccine and will resolve within a few days. A cool, damp cloth or wrapped ice pack where the vaccine was given may help. \n--These local injection reactions will go away on their own; however you may feel unwell for a day or two. If you are unable to carry on with your regular activities because of these symptoms, you can take medication such as acetaminophen (Tylenol, Tempra) or ibuprofen (Advil, Motrin). Check with your health care provider if you need advice about medication. \n\n**OTHER SIDE EFFECTS MAY INCLUDE:** \n\n --Tiredness, headache, fever, chills, muscle or joint soreness, nausea and vomiting.\n--These side effects will go away on their own; however you may feel unwell for a day or two. If you are unable to carry on with your regular activities because of these side effects, you can take medication such as acetaminophen (Tylenol, Tempra) or ibuprofen (Advil, Motrin). Check with your health care provider if you need advice about medication.")

    if message.content=='$se Pfizer'or message.content=='$se moderna' or message.content=='$se janseen'or message.content=='$se AstraZeneca' :
        await message.channel.send("IN THE ARM WHERE YOU GOT THE SHOT \n\nPain\nRedness\nSwelling \n\nTHROUGHOUT THE REST OF YOUR BODY \n\nTiredness\nHeadache\nMuscle pain\nChills\nFever\nNausea \n\nThese side effects usually start within a day or two of getting the vaccine. Side effects might affect your ability to do daily activities, but they should go away in a few days. ")

client.run(BOT_TOKEN)
# print(get_number("$contact covid-BC"))

