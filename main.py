from src.engine import WyrdAI

def main():
    try:
        assistant = WyrdAI()
        chain = assistant.get_chain()
        
        print("\n--- Wyrd Wiki Local RAG Active ---")
        while True:
            query = input("\nAsk the Wiki (or 'exit'): ")
            if query.lower() == 'exit': break
            
            response = chain.invoke(query)
            print(f"\nAI: {response}")
    except Exception as e:
        print(f"Error: {e}. Did you run ingest.py first?")

if __name__ == "__main__":
    main()