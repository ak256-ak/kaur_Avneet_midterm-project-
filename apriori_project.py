import pandas as pd
from apyori import apriori
import time


def select_store():
    print("Welcome ")
    print("User please select your store:")
    print("1. Amazon")
    print("2. Acme")
    print("3. Shoprite")
    print("4. Walmart")
    print("5. Target")
    
    store_option = input("Please select the store number: ")
    
    store_dict = {
        '1': 'amazon',
        '2': 'acme',
        '3': 'shoprite',
        '4': 'walmart',
        '5': 'target'
    }
    
    return store_dict.get(store_option, 'amazon')  


def run_apriori(file_name, min_support, min_confidence):
    
    df = pd.read_csv(file_name, header=None)
    transactions = df.apply(lambda row: row.dropna().tolist(), axis=1).tolist()

    print(f"\nTotal number of transactions: {len(transactions)}")
    unique_items = set(item for transaction in transactions for item in transaction)
    print(f"Number of unique items: {len(unique_items)}")

    
    print("\nTransactions:")
    for i, transaction in enumerate(transactions, 1):
        print(f"Transaction {i}: {transaction}")

  
    start_time = time.time()

    
    results = []
    initial_support = min_support  

    
    while not results and min_support > 0.01:
     
        association_rules = apriori(transactions, min_support=min_support, min_confidence=min_confidence)
        results = list(association_rules)
        
        
        if not results:
            min_support *= 0.8
            min_confidence *= 0.8

    
    end_time = time.time()

   
    print(f"\nApriori execution time: {end_time - start_time:.4f} seconds")

    if not results:
        print(f"\nNo frequent itemsets or rules found even after lowering thresholds.")
        return

    
    print("\nFrequent Itemsets with Support Counts (L2 format):")
    for result in results:
        if len(result.items) > 1:
            print(f"Itemset: {list(result.items)}, Support: {result.support:.2%}")

    
    print("\nTop Association Rules:")
    rule_count = 0
    for result in results:
        if len(result.items) > 1:  
            for ordered_stat in result.ordered_statistics:
                if ordered_stat.confidence >= min_confidence and rule_count < 6:
                    base = list(ordered_stat.items_base)
                    add = list(ordered_stat.items_add)
                    if base and add:  
                        rule_count += 1
                        print(f"Rule {rule_count}: {base} -> {add}")
                        print(f"Support: {result.support:.2%}")
                        print(f"Confidence: {ordered_stat.confidence:.2%}")
                        print(f"Lift: {ordered_stat.lift:.2f}")
                        print('-' * 40)

    if rule_count == 0:
        print(f"\nNo association rules found with the current thresholds.")


def main():
    store = select_store()  
    file_name = f"database_{store.lower()}.csv"  
    print(f"\nYou have selected the dataset located in {file_name}")
    
    min_support = float(input("Enter the minimum support as a percentage : ")) / 100
    min_confidence = float(input("Enter the minimum confidence as a percentage : ")) / 100
    
    
    run_apriori(file_name, min_support, min_confidence)

if __name__ == "__main__":
    main()
