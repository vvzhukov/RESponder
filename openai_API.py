import json
import openai

# Load API key from json file

with open('tokens/openaikey.json', 'r') as keyf:
    openai.api_key = json.load(keyf)['key']


def openai_request(body_text):
    # Create request to API
    try:

        prompt_intro = "Based on the text delimited by ``` provide the following information: \n \
                        1. Is that a lead for potential seller/buyer? (Yes/No) \n \
                        2. What is the type of deal: (Buy/Sell/Rent/Other)? \n \
                        3. Name of the person interested in the deal? \n \
                        4. Contact information? \n \
                        5. Type of property? \n \
                        6. Size of property? \n \
                        7. Location? \n \
                        8. Budget? \n \
                        9. Prepare a draft of the response email. Pretend that you are a sales person and you are \
                        interested in the potential deal. Mention some details from the original text. \n \
                        Your response should be in JSON format with the following keys: \n \
                        'LEAD', 'DEAL_TYPE', 'CONTACT_NAME', 'CONTACT_INFO', 'PROPERTY_TYPE', 'PROPERTY_SIZE', \
                        'PROPERTY_LOCATION', 'BUDGET', 'EMAIL_DRAFT'. \n \
                        Use NA for the missing information. Use double quotes for key and value. Replace all the line breaks with \\n. \
                        Text: ``` "

        response = openai.Completion.create(model="text-davinci-003", prompt=prompt_intro + body_text + " ```",
                                            temperature=0, max_tokens=1200)
        return response['choices'][0]['text']
    except:
        return -1
