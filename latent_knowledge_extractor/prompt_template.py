#dict to store the MMP templates
#choose 3 templates for each relation
#test 10 relations which have both the HGP and MMP templates
#relation_id: 7, 12 ,32, 40, 50, 56, 65, 70, 73, 76,91, 94
#relation_name: instance of, genre, position played on team / speciality, original language of film/TV show, capital, native language, named after, official language, developer, original broadcaster, record label, manufacturer
MMP_TEMPLATES = {
    #7: instance of 
    "7":{
        "0": "{head} is a small",
        "1": "{head} and liberal",
        "2": "{head} artist",
        "3": "{head} instance of "
    },
    #12: genre
    "12":{
        "0": "{head} series of",
        "1": "{head} favorite",
        "2": "{head} is an american"
    },
    #16: language spoken, written or signed
    "16":{
        "0": None,
        "1": None,
        "2": None
    },
    #40: original language of film/TV show
    "40":{
        "0": "{head} a. r. rahman",
        "1": None,
        "2": None
    },
    #32: position played on team / speciality
    "32":{
        "0": "{head} substitutions :",
        "1": "{head} substitutes :",
        "2": None
    },
    #50: capital
    "50":{
        "0": "{head} united states embassy in",
        "1": "{head} representative legislature",
        "2": "{head} rock band from",
    },
    #56: native language
    "56":{
        "0": "{head} descent",
        "1": "{head} speak the",
        "2": "{head} population or a widely spoken"
    },
    #65: named after
    "65":{
        "0": "{head} and produces",
        "1": "{head} variety of standard )",
        "2": "{head} official"
    },
    #70: official language
    "70":{
        "0": "{head} professor of",
        "1": "{head} is the official language in",
        "2": "{head} is the official language spoken in"
    },
    #73:developer
    "73":{
        "0": "{head} was developed by",
        "1": "{head} 2008",
        "2": "{head} references external links"
    },
    #76: original broadcaster
    "76":{
        "0":"{head} premiered on",
        "1":"{head} aired on",
        "2":"{head} 2021",
    },
    #91: record label
    "91":{
        "0": "{head} signed with",
        "1": "{head} sohmed a recording contract with",
        "2": "{head} released by"
    },
    #94: manufacturer
    "94":{
        "0": "{head} attributed to the",
        "1": "{head} 113",
        "2": "{head} cedar point"
    },
}

#dict to store the HGP templates
HGP_TEMPLATES = {
    #7: instance of
    "7":{
        "0": "{head} means",
        "1": "{head} is one",
        "2": "{head} is a",
        "3": "{head} instance of",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    #12: genre
    "12":{
        "0": "{head} is playing music",
        "1": "{head} play",
        "2": "{head} performs",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    #16: language spoken, written or signed
    "16":{
        "0": "{head} used to communicate in",
        "1": "{head} in order to communicate in",
        "2": None,
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    #32: position played on team / speciality
    "32":{
        "0":"{head} plays in position",
        "1":"{head} plays at position",
        "2":"{head} is in the position",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    #40 original language of film/TV show
    "40":{
        "0": "The original language of {head} is",
        "1": "The source language of {head} is",
        "2": "The default language of {head} is",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    #50: capital
    "50":{
        "0": "The capital of {head} is",
        "1": "The capital city of {head} is",
        "2": "Its capital {head} is",
        "3": "ausicfabh sidh {head} kisfkk",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
        "5": "{head}"
    },
    #56: native language
    "56":{
        "0": "{head} is a native language of",
        "1": " The mother tongue of {head} is",
        "2": "{head} means",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    #65: named after
    "65":{
        "0": "{head} is named after",
        "1": "{head} is named for",
        "2": "{head} is called after",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    #70: official language
    "70":{
        "0": " The official language {head} is",
        "1": "{head} is",
        "2": "{head} is officially",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    #73:developer
    "73":{
        "0": "{head} is developed by",
        "1": "{head} is created by",
        "2": "{head} is designed by",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    #76: original broadcaster
    "76":{
        "0": "{head} was originally aired on",
        "1": "{head} was originally broadcast on",
        "2": "{head} was originally shown in",
        "3": "{head} jsiaoc oeprjf iafhds of",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    #91: record label
    "91":{
        "0": "{head} is signed to",
        "1": "{head} is a recording artist for",
        "2": "{head} is a recording artist on",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    #94: manufacturer
    "94":{
        "0": "{head} is represented by music label",
        "1": "{head} is represented by the record label",
        "2": "{head} is represented by",
        "4": "jfann skfnaj aiohf aoijd aoijdakf oaisj alijf {head}, falajsdbf akfbjeba akufakcjsb aksjfbakjs kajsfbak kajsbfjsk uwfurgw ysgf",
    },
    "8":{
        "0": "{head} date of birth"
    },
    "0":{
        "0": "{head} was born in the year of",
        "1": "{head} saifhjdk afknajn ejfbk jenf",
        "2": "The year a person born in the year {head} turns 10 is the year",
        "3": "{head} aahhbsii djkqbejkq ekjf jedk",
        "4": "{head} saifhjdk afknajn ejfbk jenf aahhbsii djkqbejkq ekjf jedk",
    }
}

