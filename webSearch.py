from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
import os

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

search = GoogleSerperAPIWrapper()

# testing the google search API
results = search.run(query="What are the various vaccines of COVID-19")
print(results)


"""

# Results from the google search API:
Different types of COVID-19 vaccines: How they work ·
 mRNA vaccine · mRNA vaccine · Messenger RNA (mRNA) vaccine · Viral vector vaccine · 
 Viral vector vaccine ... Two types of COVID-19 vaccines are recommended for use in the United States: 
 mRNA vaccines (Moderna and Pfizer-BioNTech) and a protein subunit ... First introduced in December 2020, 
 the original COVID mRNA vaccines from both Pfizer and Moderna protected 
 against the original SARS-CoV-2 virus ... On this page, you will find infographics to explain how different types of vaccines work, 
 including the Pfizer/BioNTech vaccine, the Moderna vaccine and the ... Schedule your COVID-19 vaccine at CVS Pharmacy. Moderna,
  Pfizer-BioNTech and Novavax vaccines are available. No cost with most insurance. List of COVID-19 vaccine authorizations · 
  1 Overview maps · 2 Oxford–AstraZeneca · 3 Pfizer–BioNTech. 3.1 Original; 3.2 Bivalent original–BA.1; 3.3 Bivalent ... 
  CDC recommends a 2025-2026 COVID-19 vaccine for people ages 6 months and older based on individual-based decision-making. The COVID-19 ... 
  WHO recommends a simplified single-dose regime for primary immunization for most COVID-19 vaccines which would improve acceptance and uptake and provide ... 
  12 Vaccines Granted Emergency Use Listing (EUL) by WHO. Novavax. Nuvaxovid. Approved in 40 countries. 22 trials in 14 countries. COVID vaccines train your immune system to fight off COVID-19. Most work by giving your body a set of instructions (mRNA
  ) to make a harmless piece of the ...
"""