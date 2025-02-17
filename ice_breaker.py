from typing import Tuple
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from chains.custom_chains import (
    get_summary_chain,
    get_interests_chain,
    get_ice_breaker_chain,
)

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from output_parsers import (
    summary_parser,
    topics_of_interest_parser,
    ice_breaker_parser,
    Summary,
    IceBreaker,
    TopicOfInterest,
)

#For importing all environment variables
from dotenv import load_dotenv
load_dotenv()


def ice_break_with(name: str) -> Tuple[Summary, IceBreaker, TopicOfInterest, str]:

    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username)

    summary_chain = get_summary_chain()
    summary_and_facts = summary_chain.run(
        information=linkedin_data, twitter_posts=tweets
    )
    summary_and_facts = summary_parser.parse(summary_and_facts)

    interests_chain = get_interests_chain()
    interests = interests_chain.run(information=linkedin_data, twitter_posts=tweets)
    interests = topics_of_interest_parser.parse(interests)

    ice_breaker_chain = get_ice_breaker_chain()
    ice_breakers = ice_breaker_chain.run(
        information=linkedin_data, twitter_posts=tweets
    )
    ice_breakers = ice_breaker_parser.parse(ice_breakers)

    return (
        summary_and_facts,
        interests,
        ice_breakers,
        linkedin_data.get("profile_pic_url"),
    )


# from langchain import PromptTemplate
# from langchain.chains import LLMChain
# from langchain.chat_models import ChatOpenAI
# from third_parties.linkedin import scrape_linkedin_profile



# information = """
#     Bhagat Singh (27 September 1907[1] – 23 March 1931) was a charismatic Indian revolutionary[3] who participated in the mistaken murder of a junior British police officer[4] in what was to be retaliation for the death of an Indian nationalist.[5] He later took part in a largely symbolic bombing of the Central Legislative Assembly in Delhi and a hunger strike in jail, which—on the back of sympathetic coverage in Indian-owned newspapers—turned him into a household name in the Punjab region, and after his execution at age 23 into a martyr and folk hero in Northern India.[6] Borrowing ideas from Bolshevism and anarchism,[7] he electrified a growing militancy in India in the 1930s, and prompted urgent introspection within the Indian National Congress's nonviolent but eventually successful campaign for India's independence.[8]

# In December 1928, Bhagat Singh and an associate, Shivaram Rajguru, both members of a small revolutionary group, the Hindustan Socialist Republican Association (also Army, or HSRA), shot dead a 21-year-old British police officer, John Saunders, in Lahore, Punjab, in what is today Pakistan, mistaking Saunders, who was still on probation, for the British senior police superintendent, James Scott, whom they had intended to assassinate.[9] They held Scott responsible for the death of a popular Indian nationalist leader Lala Lajpat Rai for having ordered a lathi (baton) charge in which Rai was injured and two weeks thereafter died of a heart attack. As Saunders exited a police station on a motorcycle, he was felled by a single bullet fired from across the street by Rajguru, a marksman.[10][11] As he lay injured, he was shot at close range several times by Singh, the postmortem report showing eight bullet wounds.[12] Another associate of Singh, Chandra Shekhar Azad, shot dead an Indian police head constable, Channan Singh, who attempted to give chase as Singh and Rajguru fled.[10][11]

# After having escaped, Bhagat Singh and his associates used pseudonyms to publicly announce avenging Lajpat Rai's death, putting up prepared posters that they had altered to show John Saunders as their intended target instead of James Scott.[10] Singh was thereafter on the run for many months, and no convictions resulted at the time. Surfacing again in April 1929, he and another associate, Batukeshwar Dutt, set off two low-intensity homemade bombs among some unoccupied benches of the Central Legislative Assembly in Delhi. They showered leaflets from the gallery on the legislators below, shouted slogans, and allowed the authorities to arrest them.[13] The arrest, and the resulting publicity, brought to light Singh's complicity in the John Saunders case. Awaiting trial, Singh gained public sympathy after he joined fellow defendant Jatin Das in a hunger strike, demanding better prison conditions for Indian prisoners, the strike ending in Das's death from starvation in September 1929.

# Bhagat Singh was convicted of the murder of John Saunders and Channan Singh, and hanged in March 1931, aged 23. He became a popular folk hero after his death. Jawaharlal Nehru wrote about him: "Bhagat Singh did not become popular because of his act of terrorism but because he seemed to vindicate, for the moment, the honour of Lala Lajpat Rai, and through him of the nation. He became a symbol; the act was forgotten, the symbol remained, and within a few months each town and village of the Punjab, and to a lesser extent in the rest of northern India, resounded with his name."[14] In still later years, Singh, an atheist and socialist in adulthood, won admirers in India from among a political spectrum that included both communists and right-wing Hindu nationalists. Although many of Singh's associates, as well as many Indian anti-colonial revolutionaries, were also involved in daring acts and were either executed or died violent deaths, few came to be lionised in popular art and literature as did Singh, who is sometimes referred to as the Shaheed-e-Azam ("Great martyr" in Urdu and Punjabi).[15]
# """

if __name__ == "__main__":

    pass

    # print("Hello Langchain")
    # linkedin_data = scrape_linkedin_profile(
    #     "https://www.linkedin.com/in/harrison-chase-961287118/"
    # )
    # print(linkedin_data)
    # summary_template = """
    #     given the information {information} about a person I want you to give:
    #     1. a short summary.
    #     2. two interesting facts about them.
    # """

    # # infomration is the input variable embedded in  summary template
    # summary_prompt_template = PromptTemplate(
    #     input_variables=["information"], template=summary_template
    # )

    # # Chat model ,higher the temperature more creativity
    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # # initialize a chain
    # chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    # # run the chain
    # print(chain.run(information=linkedin_data))
