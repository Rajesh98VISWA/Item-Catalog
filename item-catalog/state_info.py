from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_set import Country, Base, State, User
engine = create_engine('sqlite:///stateslist.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(
  name="Rajesh Viswa",
  email="viswanadharajesh@gmail.com",
  picture="https://lh3.googleusercontent.com/-b3nsOibSCTg"
          "/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3re8fc_B6-6UcvyuxlZ2AiAvaliYbQ"
          "/s48-c-mo/photo.jpg")
session.add(User1)
session.commit()


country1 = Country(name="North_India", user_id=1)
session.add(country1)
session.commit()

state1 = State(
  name="Jammu and Kashmir",
  about="Jammu and Kashmir ,is a state in northern India"
        "often denoted by its acronym, J&K."
        " It is located mostly in the Himalayan"
        "mountains,"
        "and shares borders with the states of"
        "Himachal Pradesh and Punjab to the south."
        "The Line of Control separates it from the"
        "Pakistani-administered territories of Azad"
        "Kashmir",
  State_capital="Shimla",
  State_culture="Buddist, Hinduism, Christianity",
  State_Language="Urdu, Kashmiri",
  State_population="6,864,602",
  State_area="55,673 sqkm(21,495 sq mi)",
  districts="22",
  state_id=1,
  user_id=1
  )
session.add(state1)
session.commit()

state2 = State(
    name="Himachal Pradesh",
    about="Himachal Pradesh ,is a state in"
          "northern part of India."
          "Situated in the Western Himalayas,it is"
          "bordered by states of Jammu and Kashmir"
          "on the north, Punjab on the west,"
          "Haryana on the southwest, Uttarakhand on"
          "the southeast, and Tibet on the east."
          "At its southernmost point,"
          "it also touches the state of "
          "Uttar Pradesh."
          "The state's name was coined from the"
          "Sanskrit Him means 'snow' and"
          "achal means land",
    State_capital="Shimla",
    State_culture="Buddist, Hinduism, Christianity",
    State_Language="Urdu, Kashmiri",
    State_population="6,864,602",
    State_area="55,673 sqkm(21,495 sq mi)",
    districts="22",
    state_id=1,
    user_id=1
    )
session.add(state2)
session.commit()


state3 = State(
    name="Haryana",
    about="carved out of the former state of East Punjab on 1 November 1966"
    "on linguistic as well as on cultural basis,"
    "is one of the 29 states in India."
    "Situated in North India with less than 1.4%"
    "(44,212 km2 (17,070 sq mi)) of India's land area,"
    "it is ranked 22nd in terms of area."
    "Faridabad in National Capital Region is the most populous"
    "city of the state"
    "and Gurugram is a leading financial hub of NCR with major"
    "Fortune 500 companies located in it."
    "Haryana has 6 administrative divisions, 22 districts, 72"
    "sub-divisions, 93 revenue tehsils,"
    "50 sub-tehsils, 140 community development blocks, 154 cities and towns,"
    "6,848 villages and 6222 villages panchayats.",
    State_capital="Chandigarh",
    State_culture="Buddist, Hinduism, Christianity",
    State_population="25,353,081",
    State_Language="Hindi,Punjabi",
    State_area="44,212 km2 (17,070 sq mi)",
    districts="22",
    state_id=1,
    user_id=1
    )
session.add(state3)
session.commit()

country2 = Country(name="South_India")
session.add(country2)
session.commit()

state1 = State(
    name="Telangana",
    about="is a state in India situated on the centre-south"
    "stretch of the Indian "
    "peninsula on the high Deccan Plateau.It is the twelfth"
    "largest state and the "
    "twelfth-most populated state in India On 2 June 2014, the"
    "area was separated "
    "from the northwestern part of Andhra Pradesh as the newly"
    "formed 29th state"
    "with Hyderabad as its historic permanent capital.Its other major cities "
    "include Warangal, Nizamabad, Khammam and Karimnagar.As"
    "of 2019, the state of"
    "Telangana is divided into 33 districts.",
    State_capital="Hyderabad",
    State_culture="Hinduism,Muslim,Christianity",
    State_population="35,193,978",
    State_Language="Punjabi,Urdu ",
    State_area="112,077 km2 (43,273 sq mi)",
    districts="22",
    state_id=2,
    user_id=1
    )
session.add(state1)
session.commit()

state2 = State(
    name="Karnataka",
    about="is a state in the south western region of India."
    "It was formed on 1 November 1956,with the passage of "
    "the States Reorganisation Act.Originally known as the"
    "State of Mysore,it was renamed Karnataka in 1973."
    "The state corresponds to the Carnatic region."
    "The capital and largest city is Bangalore (Bengaluru)."
    "Karnataka is the eighth largest state by population."
    "Karnataka also has the only 3 naturally Sanskrit-speaking"
    "districts in India",
    State_capital="Bangalore",
    State_culture="Hinduism,Muslim,Christianity,Jainism",
    State_population="61,130,704",
    State_Language="Kannada",
    State_area="191,791 km2 (74,051 sq mi)",
    districts="30",
    state_id=2,
    user_id=1
    )
session.add(state2)
session.commit()

state3 = State(
    name="Telangana",
    about="is a state in India situated on the centre-south"
    "stretch of the Indian "
    "peninsula on the high Deccan Plateau.It is the twelfth"
    "largest state and the "
    "twelfth-most populated state in India On 2 June 2014,"
    "the area was separated "
    "from the northwestern part of Andhra Pradesh as the newly"
    "formed 29th state"
    "with Hyderabad as its historic permanent capital."
    "Its other major cities "
    "include Warangal, Nizamabad, Khammam and Karimnagar."
    "As of 2019, the state of"
    "Telangana is divided into 33 districts.",
    State_capital="Hyderabad",
    State_culture="Hinduism,Muslim,Christianity,",
    State_population="28,553,231",
    State_Language="Punjabi,Urdu ",
    State_area="355,591 km2 (137,294 sq mi)",
    districts="30",
    state_id=2,
    user_id=1
    )
session.add(state3)
session.commit()

print("List of States added!!!")
