import itertools
import pandas as pd
import time

def select_store():
    stores = ['Amazon', 'Acme', 'Shoprite', 'Walmart', 'Target']
    print("Available stores:")
    for i, store in enumerate(stores, 1):
        print(f"{i}. {store}")
    while True:
        try:
            store_num = int(input("Select store (1-5): "))
            if 1 <= store_num <= 5:
                selected_store = stores[store_num - 1]
                print(f"\nSelected Store: {selected_store}")
                return selected_store
            else:
                print("Please choose a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def count_itemsets(transactions, itemset):
    count = 0
    for transaction in transactions:
        if set(itemset).issubset(transaction):
            count += 1
    return count

def brute_force(transactions, min_support):
    items = set(itertools.chain(*transactions))
    itemsets, k = [], 1
    print("\nRunning Brute Force method")
    while True:
        candidate_combinations = []
        for combo in itertools.combinations(items, k):
            support = count_itemsets(transactions, combo) / len(transactions)
            if support >= min_support:
                candidate_combinations.append((combo, support))
                print(f"Found candidate: {combo} with support {support:.2%}")  
        if not candidate_combinations:
            break
        itemsets.extend(candidate_combinations)
        k += 1
    return itemsets

def main():
    store = select_store()
    file_name = f"database_{store.lower()}.csv"
    min_support = float(input("Enter minimum support as a percentage: ")) / 100
    start_time = time.time()
    
    df = pd.read_csv(file_name, header=None)
    transactions = df.apply(lambda x: x.dropna().tolist(), axis=1).tolist()
    print(f"\nTransactions: {transactions}")  

    frequent_itemsets = brute_force(transactions, min_support)
    
    if frequent_itemsets:
        print("\nFrequent Itemsets found by Brute Force:")
        for itemset, support in frequent_itemsets:
            print(f"Itemset: {itemset} | Support: {support:.2%}")
    else:
        print("No frequent itemsets found in Brute Force method.")
    
    execution_time = time.time() - start_time
    print(f"\nBrute Force execution completed in {execution_time:.4f} seconds")

if __name__ == "__main__":
    main()
