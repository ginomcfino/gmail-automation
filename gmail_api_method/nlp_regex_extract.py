import spacy
from spacy.cli import download

model_name = "en_core_web_sm" # sample text dataset from web content
# NOTE: python -m spacy download en_core_web_sm (alternative download)

# Check if the model is installed, and if not, download it
if not spacy.util.is_package(model_name):
    print(f"Downloading spaCy model '{model_name}'...")
    download(model_name)

# load the English language model
nlp = spacy.load("en_core_web_sm")


# Function to extract stock symbols
def extract_stock_symbols(text):
    doc = nlp(text)
    stock_symbols = set()
    
    # NOTE: due to limitations, need to keep my own list of non-stock symbols
    non_stock_symbols = ['PM', 'AM', 'A', 'IRA', 'ET', 'EDT', 'EST', 'ETF', 'USDC', 'FTX', 'SMS'] # will expand to cover undetermined behaviors based on user, Robinhood, etc.
    
    for token in doc:
        if token.is_alpha and token.is_upper and token.text not in non_stock_symbols:
            stock_symbols.add(token.text)
    return list(stock_symbols)

def spacy_extract(trade_confirmations):

    # Extract stock symbols from each trade confirmation
    my_stock_symbols = []
    failed_idxs = []
    for i, confirmation in enumerate(trade_confirmations, start=0):
        symbols = extract_stock_symbols(confirmation)
        if symbols:
            my_stock_symbols += symbols
        else:
            failed_idxs.append([i])
        # if symbols:
        #     print(f'Trade Confirmation {i}: {", ".join(symbols)}')
    return list(set(my_stock_symbols)), failed_idxs



# def nlp_extract(trade_confirmations):
#     # nlp = spacy.load("en_core_web_sm")
#     # alternatively,
#     nlp = en_core_web_sm.load()

#     # store entropies from spacy model
#     # trade_confirmations = []
#     failed_ents = []
#     all_ents = []

#     traded_stock_symbols = []
#     all_stock_symbols = []

#     # ***
#     for text in trade_confirmations:
#         doc = nlp(text)

#         # trade_confirmation = {
#         #     "action": None,
#         #     "quantity": None,
#         #     "symbol": None,
#         #     "price": None,
#         #     "date": None,
#         #     "time": None,
#         # }
        
#         doc_ent = []
#         failed_doc_ents = []

#         for ent in doc.ents:
#             # if "buy" in ent.text.lower() or "sell" in ent.text.lower():
#             #     trade_confirmation["action"] = ent.text.lower()
#             # if ent.label_ == "CARDINAL":
#             #     trade_confirmation["quantity"] = int(ent.text)
#             # if ent.label_ == "MONEY":
#             #     trade_confirmation["price"] = float(ent.text.replace("$", ""))
#             # if "/" in ent.text and len(ent.text.split("/")) == 3:
#             #     trade_confirmation["symbol"] = ent.text
#             # if ent.label_ == "DATE":
#             #     trade_confirmation["date"] = ent.text
#             # if ":" in ent.text:
#             #     trade_confirmation["time"] = ent.text
#             # else:
#             #     failed_doc_ents.append(ent)
#             doc_ent.append(ent)
            
                

#         # Check if the trade confirmation has essential information
#         if all(value is None for value in trade_confirmation.values()) is not True:
#             trade_confirmations.append(trade_confirmation)

#         all_ents.append(doc_ent)
#         failed_ents.append(failed_doc_ents)

#     # ***

#     return traded_stock_symbols, all_stock_symbols